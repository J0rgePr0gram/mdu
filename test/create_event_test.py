from datetime import datetime, timedelta




def test_create_event():
    """
    Crea un evento real en Google Calendar para verificar
    que la integración funciona correctamente.
    """

    start = datetime.now() + timedelta(minutes=5)
    end = start + timedelta(minutes=45)

    event = create_event(
        title="🧪 MDU Test",
        start_datetime=start,
        end_datetime=end,
    )

    assert event is not None
    assert "id" in event

    print("\nEvento creado correctamente")
    print(f"ID: {event['id']}")
    print(f"Link: {event.get('htmlLink')}")