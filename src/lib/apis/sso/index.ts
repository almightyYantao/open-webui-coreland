import { WEBUI_API_BASE_URL } from '$lib/constants';

export const sso_auth_function = async (token:string) => {
    let error = null;

    const res = await fetch(`${WEBUI_API_BASE_URL}/auths/sso_auth?token=${encodeURIComponent(token)}`, {
        method: 'GET',
        credentials: 'include',
    })
        .then(async (res) => {
            if (!res.ok) throw await res.json();
            return res.json();
        })
        .catch((err) => {
            console.log(err);

            error = err.detail;
            return null;
        });

    if (error) {
        throw error;
    }

    return res;
};