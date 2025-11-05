<script>
	import { sso_auth_function } from '$lib/apis/sso';
	import { onMount, getContext } from 'svelte';
	import { getSsoRedirectUrl } from './sso';
	import { goto } from '$app/navigation';
	import { toast } from 'svelte-sonner';
	import { config, user, socket } from '$lib/stores';
	import { getBackendConfig } from '$lib/apis';

	let loaded = false;
	const i18n = getContext('i18n');

	const setSessionUser = async (sessionUser) => {
		if (sessionUser) {
			console.log(sessionUser);
			toast.success($i18n.t(`You're now logged in.`));
			if (sessionUser.token) {
				localStorage.token = sessionUser.token;
			}

			// @ts-ignore
			$socket.emit('user-join', { auth: { token: sessionUser.token } });
			await user.set(sessionUser);
			await config.set(await getBackendConfig());
			goto('/');
		}
	};

	onMount(async () => {
		const urlParams = new URLSearchParams(window.location.search);
		const token = urlParams.get('token');
		const cookie = urlParams.get('cookie');
		if (token) {
			// Do something with the token
			document.cookie = 'qunheinternalsso=' + token + '; path=/; Secure; HttpOnly; SameSite=None';
			sso_auth_function(token).then(async (data) => {
				await setSessionUser(data);
			});
			loaded = true;
		} else {
			window.location.href = getSsoRedirectUrl();
		}
	});
</script>
