from pymongo import MongoClient
import os
import random
import uuid
import sys
from datetime import datetime, timedelta
from faker import Faker

MONGO_URI = os.getenv("MONGO_URI", "mongodb://admin:admin@mongo:27017")
client = MongoClient(MONGO_URI)
db = client.getDatabase(os.getenv("MONGO_DB"))

fake = Faker()


def get_count(var_name, default):
    return int(os.getenv(var_name, default))


users = [str(uuid.uuid4()) for _ in range(get_count("DATAGEN_USERS_COUNT", 1000))]
products = [str(uuid.uuid4()) for _ in range(get_count("DATAGEN_PRODUCTS_COUNT", 500))]


def generate_user_sessions():
    session_counts = get_count("DATAGEN_USER_SESSIONS_COUNT", 3000)
    return [{
        "session_id": str(uuid.uuid4()),
        "user_id": random.choice(users),
        "start_time": (start_time := fake.date_time_this_year()).isoformat(),
        "end_time": (start_time + timedelta(minutes=random.randint(5, 240))).isoformat(),
        "pages_visited": [fake.uri_path() for _ in range(random.randint(1, 25))],
        "device": fake.user_agent(),
        "actions": [fake.word() for _ in range(random.randint(1, 5))]
    } for _ in range(session_counts)]


def generate_product_price_history():
    histories_count = get_count("DATAGEN_PRODUCT_PRICE_HISTORY_COUNT", 1000)
    return [{
        "product_id": random.choice(products),
        "price_changes": [{
            "date": (datetime.now() - timedelta(days=i)).isoformat(),
            "price": round(random.uniform(10, 1000), 2)
        } for i in range(random.randint(1, 10))],
        "current_price": round(random.uniform(10, 1000), 2),
        "currency": "USD"
    } for _ in range(histories_count)]


def generate_event_logs():
    logs_count = get_count("DATAGEN_EVENT_LOGS_COUNT", 3000)
    event_types = ["login", "logout", "purchase", "error", "click"]
    return [{
        "event_id": str(uuid.uuid4()),
        "timestamp": fake.date_time_this_year().isoformat(),
        "event_type": random.choice(event_types),
        "details": fake.sentence()
    } for _ in range(logs_count)]


def generate_support_tickets():
    tickets_count = get_count("DATAGEN_SUPPORT_TICKETS_COUNT", 500)
    statuses = ["open", "closed", "pending"]
    issues = ["login issue", "payment failure", "bug report", "feature request"]
    return [{
        "ticket_id": str(uuid.uuid4()),
        "user_id": random.choice(users),
        "status": random.choice(statuses),
        "issue_type": random.choice(issues),
        "messages": [fake.sentence() for _ in range(random.randint(1, 5))],
        "created_at": fake.date_time_this_year().isoformat(),
        "updated_at": fake.date_time_this_year().isoformat()
    } for _ in range(tickets_count)]


def generate_user_recommendations():
    user_recommendations_count = get_count("DATAGEN_USER_RECOMMENDATIONS_COUNT", 2000)
    return [{
        "user_id": random.choice(users),
        "recommended_products": [random.choice(products) for _ in range(random.randint(1, 5))],
        "last_updated": fake.date_time_this_year().isoformat()
    } for _ in range(user_recommendations_count)]


def generate_moderation_queue():
    moderation_queues_count = get_count("DATAGEN_MODERATION_QUEUE_COUNT", 500)
    statuses = ["pending", "approved", "rejected"]
    return [{
        "review_id": str(uuid.uuid4()),
        "user_id": random.choice(users),
        "product_id": random.choice(products),
        "review_text": fake.text(),
        "rating": random.randint(1, 5),
        "moderation_status": random.choice(statuses),
        "flags": [fake.word() for _ in range(random.randint(0, 3))],
        "submitted_at": fake.date_time_this_year().isoformat()
    } for _ in range(moderation_queues_count)]


def generate_search_queries():
    search_queries_count = get_count("DATAGEN_SEARCH_QUERIES_COUNT", 1500)
    return [{
        "query_id": str(uuid.uuid4()),
        "user_id": random.choice(users),
        "query_text": fake.sentence(),
        "timestamp": fake.date_time_this_year().isoformat(),
        "filters": [fake.word() for _ in range(random.randint(0, 3))],
        "results_count": random.randint(0, 50)
    } for _ in range(search_queries_count)]


def generate_data_for_collections():
    db.user_sessions.insert_many(generate_user_sessions())

    db.product_price_history.insert_many(generate_product_price_history())

    db.event_logs.insert_many(generate_event_logs())

    db.support_tickets.insert_many(generate_support_tickets())

    db.user_recommendations.insert_many(generate_user_recommendations())

    db.moderation_queue.insert_many(generate_moderation_queue())

    db.search_queries.insert_many(generate_search_queries())

