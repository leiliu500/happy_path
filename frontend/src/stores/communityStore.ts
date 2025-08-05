import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export interface CommunityPost {
  id: string;
  authorId: string;
  authorName: string;
  content: string;
  type: 'support' | 'milestone' | 'question' | 'resource';
  timestamp: string;
  likes: number;
  comments: number;
  isAnonymous: boolean;
  tags: string[];
}

export interface CommunityGroup {
  id: string;
  name: string;
  description: string;
  memberCount: number;
  type: 'support' | 'challenge' | 'interest' | 'demographic';
  isJoined: boolean;
  posts: CommunityPost[];
}

export interface CommunityState {
  groups: CommunityGroup[];
  joinedGroups: string[];
  recentPosts: CommunityPost[];
  userPosts: CommunityPost[];
  isLoading: boolean;
  error: string | null;
}

export interface CommunityActions {
  joinGroup: (groupId: string) => void;
  leaveGroup: (groupId: string) => void;
  createPost: (post: Omit<CommunityPost, 'id' | 'timestamp' | 'likes' | 'comments'>) => void;
  likePost: (postId: string) => void;
  addComment: (postId: string, comment: string) => void;
  setGroups: (groups: CommunityGroup[]) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
}

export type CommunityStore = CommunityState & CommunityActions;

const initialState: CommunityState = {
  groups: [],
  joinedGroups: [],
  recentPosts: [],
  userPosts: [],
  isLoading: false,
  error: null,
};

export const useCommunityStore = create<CommunityStore>()(
  persist(
    (set, get) => ({
      ...initialState,
      
      joinGroup: (groupId: string) =>
        set((state) => ({
          joinedGroups: [...state.joinedGroups, groupId],
          groups: state.groups.map(group =>
            group.id === groupId 
              ? { ...group, isJoined: true, memberCount: group.memberCount + 1 }
              : group
          )
        })),
      
      leaveGroup: (groupId: string) =>
        set((state) => ({
          joinedGroups: state.joinedGroups.filter(id => id !== groupId),
          groups: state.groups.map(group =>
            group.id === groupId 
              ? { ...group, isJoined: false, memberCount: Math.max(group.memberCount - 1, 0) }
              : group
          )
        })),
      
      createPost: (post: Omit<CommunityPost, 'id' | 'timestamp' | 'likes' | 'comments'>) => {
        const newPost: CommunityPost = {
          ...post,
          id: `post_${Date.now()}`,
          timestamp: new Date().toISOString(),
          likes: 0,
          comments: 0,
        };
        
        set((state) => ({
          recentPosts: [newPost, ...state.recentPosts],
          userPosts: [newPost, ...state.userPosts],
        }));
      },
      
      likePost: (postId: string) =>
        set((state) => ({
          recentPosts: state.recentPosts.map(post =>
            post.id === postId ? { ...post, likes: post.likes + 1 } : post
          ),
          userPosts: state.userPosts.map(post =>
            post.id === postId ? { ...post, likes: post.likes + 1 } : post
          ),
        })),
      
      addComment: (postId: string, comment: string) =>
        set((state) => ({
          recentPosts: state.recentPosts.map(post =>
            post.id === postId ? { ...post, comments: post.comments + 1 } : post
          ),
          userPosts: state.userPosts.map(post =>
            post.id === postId ? { ...post, comments: post.comments + 1 } : post
          ),
        })),
      
      setGroups: (groups: CommunityGroup[]) => set({ groups }),
      setLoading: (loading: boolean) => set({ isLoading: loading }),
      setError: (error: string | null) => set({ error }),
    }),
    {
      name: 'community-store',
      partialize: (state) => ({
        joinedGroups: state.joinedGroups,
        userPosts: state.userPosts,
      }),
    }
  )
);
