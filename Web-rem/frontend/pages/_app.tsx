import React from "react";
import type { AppProps } from 'next/app';
import { ProvideAuth } from '../services/useAuth';
import 'tailwindcss/base.css';

function MyApp( { Component, pageProps} : AppProps ) {
    return <ProvideAuth>
        <Component {...pageProps}>

        </Component>
    </ProvideAuth>
}

export default MyApp


