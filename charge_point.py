import asyncio
import logging
import time
try:
    import websockets
except ModuleNotFoundError:
    print("This example relies on the 'websockets' package.")
    print("Please install it by running: ")
    print()
    print(" $ pip install websockets")
    import sys

    sys.exit(1)


from ocpp.v16 import ChargePoint as cp
from ocpp.v16 import call
from ocpp.v16.enums import RegistrationStatus, AuthorizationStatus

from ocpp.v16.enums import *
from ocpp.v16.datatypes import MeterValue, SampledValue
from ocpp.v16.datatypes import IdTagInfo


logging.basicConfig(level=logging.DEBUG)


class ChargePoint(cp):
    
    async def send_authorize(self):
        request = call.AuthorizePayload(
            id_tag="1234"
        #    id_tag="demo"
        )
        await asyncio.sleep(1)
        res = await self.call(request)
                
        if res.id_tag_info["status"] == AuthorizationStatus.accepted:
            print("Authorized Success")
        
        
    async def send_notify_status(self):
        request = call.StatusNotificationPayload(
         connector_id=1, error_code="NoError",   status="Available"
        )
        await asyncio.sleep(1)
        response = await self.call(request)  
        print("== Status Notify == ")    


    async def send_boot_notification(self):
        request = call.BootNotificationPayload(
            charge_point_model="Optimus", charge_point_vendor="The Mobility House"
        )

        response = await self.call(request)

        print(response)
        if response.status == RegistrationStatus.accepted:
            print("Connected to central system.")
            




async def main():
    async with websockets.connect(
        #"ws://localhost:9000/CP_1",subprotocols=["ocpp1.6"]
        "ws://35.247.92.36:9000/CP_1", subprotocols=["ocpp1.6"]
        #"ws://cubeocpp.run.goorm.io:9000/CP_1", subprotocols=["ocpp1.6"]
        #"ws://cs.ocpp-css.com:9220/ocpp/CP1", subprotocols=["ocpp1.6"]
        #"ws://css.ocpp-css.com:9220/ocpp/CP1", subprotocols=["ocpp1.6"]
    ) as ws:

       cp = ChargePoint("CP1", ws)

       await asyncio.gather(cp.start(), cp.send_boot_notification(),cp.send_authorize(),cp.send_notify_status())

if __name__ == "__main__":
    # asyncio.run() is used when running this example with Python >= 3.7v
    asyncio.run(main())
