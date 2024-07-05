import pytest

from tests.data import test_data


@pytest.mark.asyncio
async def test_item_handler(test_client):
    """test the item_handler route"""
    response = test_client.get(f"/items/{test_data.id}")
    response_data = response.json()

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert response.headers["Content-Length"] == "405"
    assert response_data["id"] == test_data.id
    assert response_data["name"] == test_data.name
    assert response_data["description"] == test_data.description
    assert response_data["price"] == test_data.price
    assert response_data["type"] == test_data.type
    assert response_data["brand"] == test_data.brand


@pytest.mark.asyncio
async def test_item_handler_404(test_client):
    """test the item_handler route with a non-existent item"""
    item_id = 10000000
    response = test_client.get(f"/items/{item_id}")

    assert response.status_code == 404
    assert response.headers["Content-Type"] == "application/json"
    assert response.headers["Content-Length"] == "45"
    assert bytes(f'{{"detail":"Item with ID {item_id} not found."}}', "utf-8") in response.content


@pytest.mark.asyncio
async def test_similar_handler(test_client):
    """test the similar_handler route"""
    response = test_client.get("/similar?id=1&n=1")

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert response.headers["Content-Length"] == "428"
    assert response.json() == [
        {
            "id": 71,
            "name": "Explorer Frost Boots",
            "price": 149.99,
            "distance": 0.47,
            "type": "Footwear",
            "brand": "Daybird",
            "description": "The Explorer Frost Boots by Daybird are the perfect companion for "
            "cold-weather adventures. These premium boots are designed with a waterproof and insulated "
            "shell, keeping your feet warm and protected in icy conditions. The sleek black design "
            "with blue accents adds a touch of style to your outdoor gear.",
        }
    ]


@pytest.mark.asyncio
async def test_similar_handler_422(test_client):
    """test the similar_handler route with missing query parameters"""
    response = test_client.get("/similar")

    assert response.status_code == 422
    assert response.headers["Content-Type"] == "application/json"
    assert response.headers["Content-Length"] == "88"
    assert b'{"detail":[{"type":"missing","loc":["query","id"]' in response.content


@pytest.mark.asyncio
async def test_similar_handler_404(test_client):
    """test the similar_handler route with a non-existent item"""
    item_id = 10000000
    response = test_client.get(f"/similar?id={item_id}&n=1")

    assert response.status_code == 404
    assert response.headers["Content-Type"] == "application/json"
    assert response.headers["Content-Length"] == "45"
    assert bytes(f'{{"detail":"Item with ID {item_id} not found."}}', "utf-8") in response.content


@pytest.mark.asyncio
async def test_chat_non_json_415(test_client):
    """test the chat route with a non-json request"""
    response = test_client.post("/chat")

    assert response.status_code == 422
    assert response.headers["Content-Type"] == "application/json"
    assert response.headers["Content-Length"] == "82"
    assert b'{"detail":[{"type":"missing"' in response.content
