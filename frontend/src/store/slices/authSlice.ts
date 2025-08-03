import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface User {
  id: number;
  username: string;
  email: string;
  token: string;
}

interface AuthState {
  user: User | null;
  isLoading: boolean;
  error: string | null;
  isAuthenticated: boolean;
}

const initialState: AuthState = {
  user: null,
  isLoading: false,
  error: null,
  isAuthenticated: localStorage.getItem('access_token') !== null,
};

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    loginStart: (state) => {
      state.isLoading = true;
      state.error = null;
    },
    loginSuccess: (state, action: PayloadAction<User>) => {
      state.isLoading = false;
      state.user = action.payload;
      state.error = null;
      state.isAuthenticated = true;
    },
    loginFailure: (state, action: PayloadAction<string>) => {
      state.isLoading = false;
      state.error = action.payload;
    },
    logout: (state) => {
      state.user = null;
      state.isLoading = false;
      state.error = null;
      state.isAuthenticated = false;
    },
    checkAuth: (state) => {
      // 检查本地token是否存在，同步认证状态
      const token = localStorage.getItem('access_token');
      state.isAuthenticated = token !== null;
    },
  },
});

export const { loginStart, loginSuccess, loginFailure, logout, checkAuth } = authSlice.actions;

export default authSlice.reducer;