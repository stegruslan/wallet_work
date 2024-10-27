import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
    vus: 1000, // количество виртуальных пользователей
    duration: '30s', // продолжительность теста
};

export default function () {
    let url = 'http://localhost:8000/api/v1/wallets/8bb06e9b-5f4e-4d0f-9f19-e5ca2e429c5b/operation';
    let payload = JSON.stringify({
        operationType: 'DEPOSIT', // или 'WITHDRAW'
        amount: 100,
    });

    let params = {
        headers: {
            'Content-Type': 'application/json',
        },
    };

    let res = http.post(url, payload, params);

    check(res, {
        'is status 200': (r) => r.status === 200, // проверка, что статус 200
    });

    sleep(1); // ожидание 1 секунды между запросами
}
