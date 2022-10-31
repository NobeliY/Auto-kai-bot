import React, {useState, useEffect, useContext, createContext} from "react";
import {useRouter} from "next/router";
import cookie from 'cookie';

const authContext = createContext();

export function ProvideAuth({ children }) {
    const auth = useProvideAuth();
    return <authContext:Provider value={auth}>{children}</authContext:Provider>
}
export const useAuth = () =>  {
    return useContext(authContext);
}

function useProvideAuth() {
    const [user, setUser] = useState(null);

    const router = useRouter();
    const login = (adminLogin, password) => fetch(`http://localhost:3000/api/login`, {
        method: 'POST',
        credentials: 'include',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-XSRF-TOKEN': cookie.parse(document.cookie)['X-XSRF-TOKEN'] || false,
        },
        body: JSON.stringify({adminLogin, password})
    }).then(data => {
        fetchUser();

        return data;
    });

    // registration admin
    const register = (adminLogin, password) => {};

    const logout = (adminLogin) => fetch(`http://localhost:3000/api/logout`, {
        method: 'POST',
        credentials: 'include',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-XSRF-TOKEN': cookie.parse(document.cookie)['X-XSRF-TOKEN'] || false,
        },
    }).then(data => {
        setUser(false);

        return data;
    });

    // resetPassword
    const sendPasswordResetEmail = {};
    const confirmPasswordReset = (code, password) => {};

    const fetchUser = async () => {
        try {
            const user = await fetch(`http://localhost:3000/api/admin`, {
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'X-XSRF-TOKEN': cookie.parse(document.cookie)['X-XSRF-TOKEN'] || false,
                },
            });

            if (user.status !== 200) {
                setUser(false);
                return;
            }

            const data = await user.json();
            setUser(data);

        }
        catch (e) {
            setUser(false);
        }
    }

    useEffect(() => {

        if (['/login', '/logout'].includes(router.pathname)) {
            return;
        }

        fetchUser();
        return () => fetchUser();
    }, []);

    return {
        user,
        login,
        logout,
        register,
        sendPasswordResetEmail,
        confirmPasswordReset,
    };

}