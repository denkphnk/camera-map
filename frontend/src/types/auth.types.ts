export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  full_name: string;
  email: string;
  password: string;
  organization?: string;
}

export interface AuthResponse {
  access_token: string;
}