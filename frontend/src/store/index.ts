import { configureStore } from '@reduxjs/toolkit';
import authReducer from './slices/authSlice';
import literatureReducer from './slices/literatureSlice';
import communityReducer from './slices/communitySlice';
import cooperationReducer from './slices/cooperationSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    literature: literatureReducer,
    community: communityReducer,
    cooperation: cooperationReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: ['persist/PERSIST'],
      },
    }),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;