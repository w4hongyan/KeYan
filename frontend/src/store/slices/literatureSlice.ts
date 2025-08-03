import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { Literature } from '../../pages/Literature';

interface LiteratureState {
  literatures: Literature[];
  isLoading: boolean;
  error: string | null;
  currentPage: number;
  total: number;
}

const initialState: LiteratureState = {
  literatures: [],
  isLoading: false,
  error: null,
  currentPage: 1,
  total: 0,
};

const literatureSlice = createSlice({
  name: 'literature',
  initialState,
  reducers: {
    fetchLiteraturesStart: (state) => {
      state.isLoading = true;
      state.error = null;
    },
    fetchLiteraturesSuccess: (state, action: PayloadAction<{
      literatures: Literature[];
      total: number;
    }>) => {
      state.isLoading = false;
      state.literatures = action.payload.literatures;
      state.total = action.payload.total;
      state.error = null;
    },
    fetchLiteraturesFailure: (state, action: PayloadAction<string>) => {
      state.isLoading = false;
      state.error = action.payload;
    },
    setCurrentPage: (state, action: PayloadAction<number>) => {
      state.currentPage = action.payload;
    },
    updateLiterature: (state, action: PayloadAction<Literature>) => {
      const index = state.literatures.findIndex(lit => lit.id === action.payload.id);
      if (index !== -1) {
        state.literatures[index] = action.payload;
      }
    },
  },
});

export const { fetchLiteraturesStart, fetchLiteraturesSuccess, fetchLiteraturesFailure, setCurrentPage, updateLiterature } = literatureSlice.actions;

export default literatureSlice.reducer;