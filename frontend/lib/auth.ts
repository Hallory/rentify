import { API_URL } from "./api";
import type { User, UserRole } from "@/types/api";

export type LoginPayload = {
    email: string;
    password: string;
}

export type TokenPair = {
    access: string;
    refresh: string;
}

export type RegisterPayload = {
    email: string;
    username: string;
    first_name: string;
    last_name: string;
    password: string;
    role: UserRole;
}

export async function login(payload: LoginPayload){
    const response = await fetch(`${API_URL}/auth/token/`, {
        method: "POST",
        headers:{
            "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
    });

    if (!response.ok) {
        throw new Error(response.statusText);
    }
    return response.json() as Promise<TokenPair>;
}

export async function getMe(accessToken: string){
    const response = await fetch(`${API_URL}/users/me/`, {
        headers:{
            Authorization: `Bearer ${accessToken}`,
        },
        cache:"no-store"
    });
    if(!response.ok){
        throw new Error(response.statusText);
    }
    return response.json() as Promise<User>;
}

export async function register(payload: RegisterPayload) {
    const response = await fetch(`${API_URL}/auth/register/`, {
        method: "POST",
        headers:{
            "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
    });

    if(!response.ok){
        const error = await response.json().catch(() => null);
        throw new Error(
            error?.email?.[0] ??
            error?.username?.[0] ??
            error?.password?.[0] ??
            error?.detail ??
            "Registration failed"
        );
    }

    return response.json() as Promise<User>;
}

