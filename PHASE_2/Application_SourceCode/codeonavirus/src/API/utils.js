export async function fetcher(url, error_message) {
    const response = await fetch(url);
    if (response.status !== 200) {
        console.warn(error_message)
        return []
    }
    return await response.json()
}

export function extractCountryAndDisease(urlParams, searchParams) {
    extractCountry(urlParams, searchParams);
    extractDisease(urlParams, searchParams);
}

export function extractCountry(urlParams, searchParams) {
    const country = searchParams.country
    if (country !== 'all countries') urlParams.push(['country', country])
}

export function extractDisease(urlParams, searchParams) {
    const disease = searchParams.disease
    if (disease !== 'all diseases') urlParams.push(['disease', disease])
}