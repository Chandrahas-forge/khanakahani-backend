import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.api.deps import get_current_user

client = TestClient(app)

# Override dependency so all endpoints requiring authentication succeed.
def fake_current_user():
    # Create a dummy user object with an id attribute.
    class DummyUser:
        id = 1
    return DummyUser()

app.dependency_overrides[get_current_user] = fake_current_user

# ----- Auth endpoint tests -----
def test_auth_register():
    data = {"email": "test@example.com", "password": "testpassword"}
    response = client.post("/auth/register", json=data)
    # Expecting HTTP 201 CREATED; adjust expectations if duplicate exists.
    assert response.status_code == 201
    res_data = response.json()
    assert "id" in res_data
    assert res_data["email"] == "test@example.com"

def test_auth_login():
    # First register the user so we can log in.
    data = {"email": "login_test@example.com", "password": "testpassword"}
    client.post("/auth/register", json=data)
    # OAuth2PasswordRequestForm is expecting form data with 'username' field.
    response = client.post("/auth/login", data={"username": data["email"], "password": data["password"]})
    assert response.status_code == 200
    res_data = response.json()
    assert "access_token" in res_data
    assert res_data["token_type"] == "bearer"

# ----- Recipe endpoint tests -----
def test_create_recipe():
    recipe_data = {
        "title": "Test Recipe",
        "cuisine": "Test Cuisine",
        "ingredients": ["ing1", "ing2"],
        "tags": "spicy",
        "steps": "mix and cook"
    }
    response = client.post("/recipes", json=recipe_data)
    assert response.status_code == 201
    res_data = response.json()
    assert res_data["title"] == recipe_data["title"]
    assert res_data["owner_id"] == 1

def test_list_recipes():
    # Create a recipe to ensure the list isn't empty.
    recipe_data = {
        "title": "List Test Recipe",
        "cuisine": "Cuisine Test",
        "ingredients": ["ingA", "ingB"],
        "tags": "savory",
        "steps": "prepare and serve"
    }
    client.post("/recipes", json=recipe_data)
    response = client.get("/recipes?cuisine=Test&page=1&limit=10")
    assert response.status_code == 200
    recipes = response.json()
    # Expect at least one recipe in the list.
    assert isinstance(recipes, list)
    assert len(recipes) >= 1

def test_get_recipe_by_id():
    # First, create a recipe.
    recipe_data = {
        "title": "Fetch Test Recipe",
        "cuisine": "Cuisine Fetch",
        "ingredients": ["ingX", "ingY"],
        "tags": "sweet",
        "steps": "bake and serve"
    }
    create_resp = client.post("/recipes", json=recipe_data)
    recipe_id = create_resp.json()["id"]
    response = client.get(f"/recipes/{recipe_id}")
    assert response.status_code == 200
    res_data = response.json()
    assert res_data["id"] == recipe_id

def test_update_recipe():
    # Create a recipe.
    recipe_data = {
        "title": "Original Recipe",
        "cuisine": "Original Cuisine",
        "ingredients": ["a", "b"],
        "tags": "original",
        "steps": "do it"
    }
    create_resp = client.post("/recipes", json=recipe_data)
    recipe_id = create_resp.json()["id"]

    update_data = {
        "title": "Updated Recipe",
        "cuisine": "Updated Cuisine",
        "ingredients": ["c", "d"],
        "tags": "updated",
        "steps": "redo it"
    }
    response = client.put(f"/recipes/{recipe_id}", json=update_data)
    assert response.status_code == 200
    res_data = response.json()
    assert res_data["title"] == update_data["title"]

def test_partial_update_recipe():
    # Create a recipe.
    recipe_data = {
        "title": "Partial Update Recipe",
        "cuisine": "CuisPartial",
        "ingredients": ["x", "y"],
        "tags": "initial",
        "steps": "initial steps"
    }
    create_resp = client.post("/recipes", json=recipe_data)
    recipe_id = create_resp.json()["id"]

    patch_data = {"tags": "patched"}
    response = client.patch(f"/recipes/{recipe_id}", json=patch_data)
    assert response.status_code == 200
    res_data = response.json()
    assert res_data["tags"] == "patched"

def test_delete_recipe():
    # Create a recipe to delete.
    recipe_data = {
        "title": "Delete Recipe",
        "cuisine": "Delete Cuisine",
        "ingredients": ["remove1", "remove2"],
        "tags": "delete",
        "steps": "delete steps"
    }
    create_resp = client.post("/recipes", json=recipe_data)
    recipe_id = create_resp.json()["id"]

    response = client.delete(f"/recipes/{recipe_id}")
    assert response.status_code == 200
    # Verify deletion by checking for a 404 response:
    get_resp = client.get(f"/recipes/{recipe_id}")
    assert get_resp.status_code == 404

def test_mark_and_remove_favorite():
    # Create a recipe.
    recipe_data = {
        "title": "Favorite Recipe",
        "cuisine": "Fav Cuisine",
        "ingredients": ["fav1", "fav2"],
        "tags": "favorite",
        "steps": "mark favorite"
    }
    create_resp = client.post("/recipes", json=recipe_data)
    recipe_id = create_resp.json()["id"]

    # Mark as favorite.
    fav_resp = client.post(f"/recipes/{recipe_id}/favorite")
    assert fav_resp.status_code == 200
    # Remove favorite.
    rem_resp = client.delete(f"/recipes/{recipe_id}/favorite")
    assert rem_resp.status_code == 200

def test_add_and_list_recipe_note():
    # Create a recipe.
    recipe_data = {
        "title": "Note Recipe",
        "cuisine": "Note Cuisine",
        "ingredients": ["note1", "note2"],
        "tags": "notes",
        "steps": "add notes"
    }
    create_resp = client.post("/recipes", json=recipe_data)
    recipe_id = create_resp.json()["id"]

    # Add a note.
    note_data = {"text": "This is a test note."}
    add_resp = client.post(f"/recipes/{recipe_id}/notes", json=note_data)
    assert add_resp.status_code == 201
    note_id = add_resp.json()["id"]

    # List notes.
    list_resp = client.get(f"/recipes/{recipe_id}/notes")
    assert list_resp.status_code == 200
    notes = list_resp.json()
    assert any(note["id"] == note_id for note in notes)