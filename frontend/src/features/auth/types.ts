export interface User {
    id: string
    email: string
    username: string
    created_at: string
    updated_at: string
  }
  
  export interface AuthResponse {
    access_token: string
    user: User
  }