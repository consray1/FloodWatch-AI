import { api } from './api'

export interface User {
  id: string
  name: string
  email: string
  phone?: string
  role?: string
  is_verified: boolean
  trust_score?: number
  created_at: string
  last_login?: string
}

export interface AuthToken {
  access_token: string
  refresh_token: string
  token_type: string
  expires_in: number
}

export const authApi = {
  register: (data: { name: string; email: string; phone?: string; password: string }) =>
    api.post<User>('/auth/register', data),

  login: (data: { email: string; password: string }) =>
    api.post<AuthToken>('/auth/login', data),

  logout: (token: string) =>
    api.post('/auth/logout', {}, token),

  me: (token: string) =>
    api.get<User>('/auth/me', token),

  refresh: (refreshToken: string) =>
    api.post<AuthToken>('/auth/refresh', { refresh_token: refreshToken }),
}