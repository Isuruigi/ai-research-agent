"""Prometheus metrics"""
from prometheus_client import Counter, Histogram, Gauge
import time

# Metrics
request_count = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

request_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint']
)

active_requests = Gauge(
    'http_requests_active',
    'Active HTTP requests'
)

agent_execution_time = Histogram(
    'agent_execution_seconds',
    'Agent execution time',
    ['node']
)
