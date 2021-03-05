import { fetcher, extractCountryAndDisease } from './utils';

export async function fetchMap(filter) {
    const url = new URL('http://127.0.0.1:5001/main/map');
    const params = [['year', filter.year], ['month', filter.month]];
    extractCountryAndDisease(params, filter);
    url.search = new URLSearchParams(params).toString();

    return await fetcher(url, "Failed to fetch map data")
}

export async function fetchSidebar(filter) {
    const url = new URL('http://127.0.0.1:5001/main/sidebar');
    const params = [['year', filter.year], ['month', filter.month]];
    extractCountryAndDisease(params, filter);
    url.search = new URLSearchParams(params).toString();
    
    return await fetcher(url, "Failed to fetch side bar data");
}

export async function fetchModal(url) {
    const url_ = new URL('http://127.0.0.1:5001/main/modal');
    const params = [['url', url]];
    url_.search = new URLSearchParams(params).toString();
    return await fetcher(url_, "Failed to fetch side bar data");
}

export async function fetchPieChartDisease(filter) {
    const url = new URL('http://127.0.0.1:5001/main/piechart/disease');
    const params = [['year', filter.year], ['month', filter.month]];
    extractCountryAndDisease(params, filter);
    url.search = new URLSearchParams(params).toString();
    
    return await fetcher(url, "Failed to fetch pie chart disease data");
}

export async function fetchComparatorActual(country, disease, source) {
    const url = new URL('http://127.0.0.1:5001/main/comparator/actual');
    const params = [];
    extractCountryAndDisease(params, {country: country, disease: disease});
    if (source !== 'All sources') params.push(['source', source]);
    url.search = new URLSearchParams(params).toString();

    const result = await fetcher(url, "Failed to fetch comparator actual data");
    for (const pair of result) {
        pair.date = new Date(pair.date, 0);
    }
    return result;
}

export async function fetchComparatorPercentage(country, disease, source) {
    const url = new URL('http://127.0.0.1:5001/main/comparator/percentage');
    const params = [];
    extractCountryAndDisease(params, {country: country, disease: disease});
    if (source !== 'All sources') params.push(['source', source]);
    url.search = new URLSearchParams(params).toString();

    const result = await fetcher(url, "Failed to fetch comparator percentage data");
    for (const pair of result) {
        pair.date = new Date(pair.date, 0);
    }
    return result;
}

// export function fetchComparatorPercentage(totalSource) {
//     return async function(country, disease, source) {
//         const url = new URL('http://127.0.0.1:5001/main/comparator/percentage');
//         const params = [];
//         extractCountryAndDisease(params, {country: country, disease: disease});
//         if (source !== 'All sources') params.push(['source', source]);
//         if (totalSource !== 'All sources') params.push(['totalSource', source]);
//         url.search = new URLSearchParams(params).toString();

//         const result = await fetcher(url, "Failed to fetch comparator percentage data");
//         for (const pair of result) {
//             pair.date = new Date(pair.date, 0);
//         }
//         return result;
//     };
// }