import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface Skill {
  id: number;
  name: string;
}

interface Post {
  id: number;
  title: string;
  content: string;
  author: { id: number; username: string };
  skills: Skill[];
  type: 'cooperation' | 'help';
  created_at: string;
  updated_at: string;
  application_count: number;
  view_count: number;
}

interface CooperationState {
  posts: Post[];
  skills: Skill[];
  isLoading: boolean;
  error: string | null;
  currentPage: number;
  total: number;
}

const initialState: CooperationState = {
  posts: [],
  skills: [],
  isLoading: false,
  error: null,
  currentPage: 1,
  total: 0,
};

const cooperationSlice = createSlice({
  name: 'cooperation',
  initialState,
  reducers: {
    fetchPostsStart: (state) => {
      state.isLoading = true;
      state.error = null;
    },
    fetchPostsSuccess: (state, action: PayloadAction<{
      results: Post[];
      count: number;
    }>) => {
      state.isLoading = false;
      state.posts = action.payload.results;
      state.total = action.payload.count;
      state.error = null;
    },
    fetchPostsFailure: (state, action: PayloadAction<string>) => {
      state.isLoading = false;
      state.error = action.payload;
    },
    fetchSkillsStart: (state) => {
      state.isLoading = true;
      state.error = null;
    },
    fetchSkillsSuccess: (state, action: PayloadAction<Skill[]>) => {
      state.isLoading = false;
      state.skills = action.payload;
      state.error = null;
    },
    fetchSkillsFailure: (state, action: PayloadAction<string>) => {
      state.isLoading = false;
      state.error = action.payload;
    },
    setCurrentPage: (state, action: PayloadAction<number>) => {
      state.currentPage = action.payload;
    },
  },
});

export const {
  fetchPostsStart,
  fetchPostsSuccess,
  fetchPostsFailure,
  fetchSkillsStart,
  fetchSkillsSuccess,
  fetchSkillsFailure,
  setCurrentPage,
} = cooperationSlice.actions;

export default cooperationSlice.reducer;