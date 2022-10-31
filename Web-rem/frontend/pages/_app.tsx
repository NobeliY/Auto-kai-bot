import React from "react";
import { AppProps } from 'next/app';
import { ProvideAuth } from '../services/useAuth';
import 'tailwindcss/base.css';

const App = ( { Component, pageProps }: AppProps ) => {
    <ProvideAuth>
        <Component {...pageProps}></Component>
    </ProvideAuth>
}


