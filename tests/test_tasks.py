def test_create_task(client, auth_header):
    response = client.post('/tasks', headers=auth_header, json={
        "title": "Buy Milk"
    })
    assert response.status_code == 201

def test_get_tasks(client, auth_header):
    # Create one first
    client.post('/tasks', headers=auth_header, json={"title": "Task 1"})
    
    response = client.get('/tasks', headers=auth_header)
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['tasks']) == 1
    assert data['tasks'][0]['title'] == "Task 1"

def test_delete_task(client, auth_header):
    # Create
    client.post('/tasks', headers=auth_header, json={"title": "Delete Me"})
    # Get ID (it will be 1 in a fresh DB)
    task_id = 1
    
    # Delete
    response = client.delete(f'/tasks/{task_id}', headers=auth_header)
    assert response.status_code == 200
    
    # Verify it's gone
    response = client.get('/tasks', headers=auth_header)
    assert len(response.get_json()['tasks']) == 0