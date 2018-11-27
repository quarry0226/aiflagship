import time
from datetime import datetime
from os import path
import sys
import grpc

sys.path.append(path.join(path.dirname(__file__), '..'))

from iclab.abc.mesh_up import calendar_pb2
from iclab.abc.mesh_up.calendar_pb2_grpc import GoogleCalendarServiceStub
from iclab.abc.common_pb2 import StringValue, DateTime

SERVER_ADDRESS = 'aif.kaist.ac.kr:50051'
KEY_AUTH_URL = 'auth_url'

def list_calendar(stub: GoogleCalendarServiceStub, user_key: str):
    for calendar in stub.ListGoogleCalendar(calendar_pb2.GoogleCalendarListQuery(email=user_key)):
        print(calendar)


def get_calendar(stub: GoogleCalendarServiceStub, user_key: str, calendar_id: str):
    print(
        stub.GetGoogleCalendar(
            calendar_pb2.GoogleCalendarSingleQuery(
                email=user_key,
                calendar_id=calendar_id
            )
        )
    )


def create_calendar(stub: GoogleCalendarServiceStub, user_key: str,
                    summary: str, description: str, location: str, timezone: str) -> str:
    new_calendar = stub.CreateGoogleCalendar(
        calendar_pb2.GoogleCalendarPostQuery(
            email=user_key,
            calendar=calendar_pb2.GoogleCalendar(
                summary=StringValue(value=summary),
                description=StringValue(value=description),
                location=StringValue(value=location),
                timezone=StringValue(value=timezone)
            )
        )
    )
    print(new_calendar)
    return new_calendar.id.value


def update_calendar(stub: GoogleCalendarServiceStub, user_key: str,
                    calendar_id: str, summary: str, description: str, location: str, timezone: str):
    print(
        stub.UpdateGoogleCalendar(
            calendar_pb2.GoogleCalendarPostQuery(
                email=user_key,
                calendar=calendar_pb2.GoogleCalendar(
                    id=StringValue(value=calendar_id),
                    summary=StringValue(value=summary),
                    description=StringValue(value=description),
                    location=StringValue(value=location),
                    timezone=StringValue(value=timezone)
                )
            )
        )
    )


def delete_calendar(stub: GoogleCalendarServiceStub, user_key: str, calendar_id: str):
    print(
        stub.DeleteGoogleCalendar(
            calendar_pb2.GoogleCalendarSingleQuery(
                email=user_key,
                calendar_id=calendar_id
            )
        )
    )


def create_event(stub: GoogleCalendarServiceStub, user_key: str, calendar_id: str,
                 summary: str, description: str, location: str, creator: str, start_time: datetime, end_time: datetime):
    event = stub.CreateGoogleCalendarEvent(
        calendar_pb2.GoogleCalendarEventPostQuery(
            email=user_key,
            calendar_id=calendar_id,
            event=calendar_pb2.GoogleCalendarEvent(
                summary=StringValue(value=summary),
                description=StringValue(value=description),
                location=StringValue(value=location),
                creator=calendar_pb2.GoogleCalendarUser(
                    email=StringValue(value="abc@abc.com"),
                    display_name=StringValue(value=creator)
                ),
                start=DateTime(
                    year=start_time.year,
                    month=start_time.month,
                    day=start_time.day,
                    hour=start_time.hour,
                    minute=start_time.minute,
                    second=start_time.second
                ),
                end=DateTime(
                    year=end_time.year,
                    month=end_time.month,
                    day=end_time.day,
                    hour=end_time.hour,
                    minute=end_time.minute,
                    second=end_time.second
                )
            )
        )
    )
    print(event)
    return event.id.value


def update_event(stub: GoogleCalendarServiceStub, user_key: str, calendar_id: str, event_id: str,
                 summary: str, description: str, location: str, creator: str, start_time: datetime, end_time: datetime):
    print(
        stub.UpdateGoogleCalendarEvent(
            calendar_pb2.GoogleCalendarEventPostQuery(
                email=user_key,
                calendar_id=calendar_id,
                event=calendar_pb2.GoogleCalendarEvent(
                    id=StringValue(value=event_id),
                    summary=StringValue(value=summary),
                    description=StringValue(value=description),
                    location=StringValue(value=location),
                    creator=calendar_pb2.GoogleCalendarUser(
                        email=StringValue(value="abc@abc.com"),
                        display_name=StringValue(value=creator)
                    ),
                    start=DateTime(
                        year=start_time.year,
                        month=start_time.month,
                        day=start_time.day,
                        hour=start_time.hour,
                        minute=start_time.minute,
                        second=start_time.second
                    ),
                    end=DateTime(
                        year=end_time.year,
                        month=end_time.month,
                        day=end_time.day,
                        hour=end_time.hour,
                        minute=end_time.minute,
                        second=end_time.second
                    )
                )
            )
        )
    )


def list_event(stub: GoogleCalendarServiceStub, user_key: str, calendar_id: str):
    for event in stub.ListGoogleCalendarEvent(
            calendar_pb2.GoogleCalendarEventListQuery(
                email=user_key,
                calendar_id=calendar_id
            )
    ):
        print(event)


def get_event(stub: GoogleCalendarServiceStub, user_key: str, calendar_id: str, event_id: str):
    print(
        stub.GetGoogleCalendarEvent(
            calendar_pb2.GoogleCalendarEventSingleQuery(
                email=user_key,
                calendar_id=calendar_id,
                event_id=event_id
            )
        )
    )


def delete_event(stub: GoogleCalendarServiceStub, user_key: str, calendar_id: str, event_id: str):
    stub.DeleteGoogleCalendarEvent(
        calendar_pb2.GoogleCalendarEventSingleQuery(
            email=user_key,
            calendar_id=calendar_id,
            event_id=event_id
        )
    )



def calendar_run(address: str, user_key):
    #user_key = "quarry0226@gmail.com"
    channel = grpc.insecure_channel(address)
    stub = GoogleCalendarServiceStub(channel)

    print("=" * 15, "Create Calendar", "=" * 15)
    calendar_id = create_calendar(stub, user_key, "test-summary", "test-description", "test-location", "Asia/Seoul")
    time.sleep(5)

    print("=" * 15, "List Calendar", "=" * 15)
    list_calendar(stub, user_key)
    time.sleep(5)

    print("=" * 15, "Get Calendar: calendar_id = {}".format(calendar_id), "=" * 15)
    get_calendar(stub, user_key, calendar_id)
    time.sleep(5)

    print("=" * 15, "Update Calendar: calendar_id = {}".format(calendar_id), "=" * 15)
    update_calendar(stub, user_key, calendar_id, "test-updated-summary",
                    "test-updated-description", "test-updated-location", "Asia/Seoul")
    time.sleep(5)

    print("=" * 15, "Create Event in calendar_id = {}".format(calendar_id), "=" * 15)
    event_id = create_event(stub, user_key, calendar_id,
                            "test-summary", "test-description", "test-location", "test-creator",
                            datetime(2018, 10, 18, 10, 10), datetime(2018, 10, 18, 10, 11)
                            )
    time.sleep(5)

    print("=" * 15, "List Event in calendar_id = {}".format(calendar_id), "=" * 15)
    list_event(stub, user_key, calendar_id)
    time.sleep(5)

    print("=" * 15, "Get Event: calendar_id = {}, event_id = {}".format(calendar_id, event_id), "=" * 15)
    get_event(stub, user_key, calendar_id, event_id)
    time.sleep(5)

    print("=" * 15, "Update Event: calendar_id = {}, event_id = {}".format(calendar_id, event_id), "=" * 15)
    update_event(stub, user_key, calendar_id, event_id,
                 "test-updated-summary", "test-updated-description", "test-updated-location", "test-updated-creator",
                 datetime(2018, 10, 18, 10, 10), datetime(2018, 10, 18, 10, 11)
                 )
    time.sleep(5)

    print("=" * 15, "Delete Event: calendar_id = {}, event_id = {}".format(calendar_id, event_id), "=" * 15)
    delete_event(stub, user_key, calendar_id, event_id)
    time.sleep(5)

    print("=" * 15, "Delete Calendar: calendar_id = {}".format(calendar_id), "=" * 15)
    delete_calendar(stub, user_key, calendar_id)
    time.sleep(5)
