import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface Question {
  id: number;
  title: string;
  content: string;
  author: { id: number; username: string };
  tags: string[];
  created_at: string;
  updated_at: string;
  answer_count: number;
  view_count: number;
}

interface CommunityState {
  questions: Question[];
  isLoading: boolean;
  error: string | null;
  currentPage: number;
  total: number;
}

const initialState: CommunityState = {
  questions: [],
  isLoading: false,
  error: null,
  currentPage: 1,
  total: 0,
};

const communitySlice = createSlice({
  name: 'community',
  initialState,
  reducers: {
    fetchQuestionsStart: (state) => {
      state.isLoading = true;
      state.error = null;
    },
    fetchQuestionsSuccess: (state, action: PayloadAction<{
      results: Question[];
      count: number;
    }>) => {
      state.isLoading = false;
      state.questions = action.payload.results;
      state.total = action.payload.count;
      state.error = null;
    },
    fetchQuestionsFailure: (state, action: PayloadAction<string>) => {
      state.isLoading = false;
      state.error = action.payload;
    },
    setCurrentPage: (state, action: PayloadAction<number>) => {
      state.currentPage = action.payload;
    },
  },
});

export const { fetchQuestionsStart, fetchQuestionsSuccess, fetchQuestionsFailure, setCurrentPage } = communitySlice.actions;

export default communitySlice.reducer;