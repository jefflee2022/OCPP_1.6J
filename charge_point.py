import asyncio
import logging
import time
from datetime import datetime
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
from ocpp.v16.enums import RegistrationStatus, AuthorizationStatus, ChargePointStatus

from ocpp.v16.enums import *
from ocpp.v16.datatypes import MeterValue, SampledValue
from ocpp.v16.datatypes import IdTagInfo


logging.basicConfig(level=logging.DEBUG)


class ChargePoint(cp):
    
    connector_ID = 1
    id_TAG = "1111222233334444"
    
    
    async def send_start_transaction()
        request = call.StartTransactionPayload(
            vendor_id="OCUBE_EV",
            message_id="getMemberUnitPrice.req", 
            data="{\"connectorId\":" + str(ChargePoint.connector_ID) + ",\"idTag\":\"" + ChargePoint.id_TAG + "\"}"
        )
        await asyncio.sleep(5)
        res = await self.call(request)

    async def send_start_transaction()
        request = call.StopTransactionPayload(
            vendor_id="OCUBE_EV",
            message_id="getMemberUnitPrice.req", 
            data="{\"connectorId\":" + str(ChargePoint.connector_ID) + ",\"idTag\":\"" + ChargePoint.id_TAG + "\"}"
        )
        await asyncio.sleep(5)
        res = await self.call(request)    
    
    async def send_data_transfer_get_unit_price(self):
        
        request = call.DataTransferPayload(
            vendor_id="OCUBE_EV",
            message_id="getMemberUnitPrice.req", 
            data="{\"connectorId\":" + str(ChargePoint.connector_ID) + ",\"idTag\":\"" + ChargePoint.id_TAG + "\"}"
        )
        await asyncio.sleep(5)
        res = await self.call(request)
    
    
    async def send_data_transfer_set_plug_state(self):
        request = call.DataTransferPayload(    
            vendor_id="OCUBE_EV",
            message_id="putConnectorPlugNotification.req",
            data="{\"connectorId\":" + str(ChargePoint.connector_ID) + ", \"timestamp\": \"" + datetime.utcnow().date().isoformat() +  "T13:56:00.410Z\"}"  #+datetime.utcnow().isoformat()+  "Z\"}"
        )
        await asyncio.sleep(7)
        res = await self.call(request)
        
    
    async def send_authorize(self):
        request = call.AuthorizePayload(
            id_tag=ChargePoint.id_TAG #"1111222233334444"
        #    id_tag="demo"
        )
        await asyncio.sleep(1)
        res = await self.call(request)
                
        if res.id_tag_info["status"] == AuthorizationStatus.accepted:
            print("Authorized Success")
        
        
    async def send_notify_status(self, cp_status ):
        request = call.StatusNotificationPayload(
         connector_id=ChargePoint.connector_ID, error_code="NoError",   status=cp_status
        )
        await asyncio.sleep(3)
        response = await self.call(request)  
        print("== Status Notify == ")    


    async def send_boot_notification(self):
        request = call.BootNotificationPayload(
            #charge_point_model="Optimus", charge_point_vendor="The Mobility House"
            charge_point_model="TEST1", charge_point_vendor="TEST1"

        )

        response = await self.call(request)

        print(response)
        if response.status == RegistrationStatus.accepted:
            print("Connected to central system.")
            




async def main():
    async with websockets.connect(
        #"ws://localhost:9000/CP_1",subprotocols=["ocpp1.6"]
        #"ws://35.247.92.36:9000/CP_1", subprotocols=["ocpp1.6"]
        "ws://180.210.83.71:8887/CPOCB0200002",subprotocols=["ocpp1.6"]
        #"ws://cubeocpp.run.goorm.io:9000/CP_1", subprotocols=["ocpp1.6"]
        #"ws://cs.ocpp-css.com:9220/ocpp/CP1", subprotocols=["ocpp1.6"]
        #"ws://css.ocpp-css.com:9220/ocpp/CP1", subprotocols=["ocpp1.6"]
    ) as ws:

       cp = ChargePoint("CP1", ws)

       await asyncio.gather(
           cp.start(), 
           cp.send_boot_notification(),
           cp.send_authorize(),
           cp.send_notify_status(ChargePointStatus.available),
           cp.send_data_transfer_get_unit_price(),
           cp.send_data_transfer_set_plug_state(), 
           cp.send_start_transaction(),
           #cp.send_meter_value(),
           
       
       )

if __name__ == "__main__":
    # asyncio.run() is used when running this example with Python >= 3.7v
    asyncio.run(main())
