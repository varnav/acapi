import { check } from 'k6';
import http from 'k6/http';
import { sleep } from 'k6';

// Function to generate random N-number
function generateRandomReg() {
    const num = Math.floor(Math.random() * 99999);
    return `N${num.toString().padStart(5, '0')}`;
}

// Generate 1000 random registrations
const registrations = Array(1000).fill(null).map(() => generateRandomReg());

export const options = {
    stages: [
        { duration: '10s', target: 100 }, // Ramp up to 100 users
        { duration: '30s', target: 100 },  // Stay at 100 users for 1 minute
        { duration: '15s', target: 150 },
        { duration: '30s', target: 150 },
        { duration: '10s', target: 0 },  // Ramp down to 0 users
    ],
    thresholds: {
        http_req_duration: ['p(95)<2000'], // 95% of requests should complete within 2s
        http_req_failed: ['rate<0.1'],     // Less than 10% of requests should fail
    },
};

export default function () {
    // Pick a random registration from our list
    const reg = registrations[Math.floor(Math.random() * registrations.length)];
    
    // Make the request
    const res = http.get(`http://127.0.0.1:8000/api/v1/ac/getbyreg?reg=${reg}`);
    
    // Check if the response was successful
    check(res, {
        'is status 200': (r) => r.status === 200,
        'is status 404': (r) => r.status === 404,
        'response time < 2s': (r) => r.timings.duration < 2000,
    });
    
    // Wait between 1-5 seconds before next request
    sleep(Math.random() * 4 + 1);
}
