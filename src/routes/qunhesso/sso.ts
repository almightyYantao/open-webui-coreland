export const getCurrentUrl = () => {
    return encodeURIComponent(window.location.href);
};

export const getCurrentUrlProtocolHost = () => {
    return `${window.location.protocol}//${window.location.host}`;
};

export const getBackUrl = () => {
    return `${getCurrentUrlProtocolHost()}/qunhesso`;
};

export function getSsoRedirectUrl(nextUrl = '') {
    let localNextUrl = nextUrl;
    if (nextUrl === '') {
        localNextUrl = getCurrentUrl();
    }
    return `https://kuauth.kujiale.com/loginpage?backurl=${getBackUrl()}&nexturl=${localNextUrl}`;
}
