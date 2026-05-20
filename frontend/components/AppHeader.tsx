"use client";

import Header from "@/app/components/Header";
import { getMe } from "@/lib/auth";
import { clearTokens, getAccessToken } from "@/lib/token";
import { User } from "@/types/api";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";


export default function AppHeader(){
    const router = useRouter();
    const [user, setUser] = useState<User | null>(null);

    useEffect(()=>{
        const accessToken = getAccessToken();

        if(!accessToken){
            return;
        }

        getMe(accessToken)
        .then(setUser)
        .catch(()=>{
            clearTokens();
            setUser(null);
        });
    },[]);

    function logout(){
        clearTokens();
        setUser(null);
        router.push("/");
        router.refresh();
    }

    return <Header user={user} onLogout={logout} />
}
