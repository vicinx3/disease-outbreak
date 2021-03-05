import { fetcher, extractCountryAndDisease } from './utils';

export async function fetchMap(filter) {
    const url = new URL('http://127.0.0.1:5001/prediction/map');
    const params = [['offset', filter.offset]];
    extractCountryAndDisease(params, filter);
    url.search = new URLSearchParams(params).toString();
    return await fetcher(url, 'Failed to fetch map data');
}

export async function fetchTable() {
    const url = new URL('http://127.0.0.1:5001/prediction/table');
    return await fetcher(url, 'Failed to fetch map data');
}