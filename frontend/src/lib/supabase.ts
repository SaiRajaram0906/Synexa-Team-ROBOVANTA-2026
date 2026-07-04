import { createBrowserClient } from '@supabase/ssr';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || '';
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || '';

const mockSupabase = {
  auth: {
    getSession: async () => ({
      data: {
        session: {
          access_token: 'dummy-token',
          user: { id: '00000000-0000-0000-0000-000000000000', email: 'demo@synexa.com' }
        }
      },
      error: null
    }),
    getUser: async () => ({
      data: {
        user: { id: '00000000-0000-0000-0000-000000000000', email: 'demo@synexa.com' }
      },
      error: null
    }),
    signInWithPassword: async ({ email }: any) => ({
      data: {
        user: { id: '00000000-0000-0000-0000-000000000000', email: email || 'demo@synexa.com' },
        session: { access_token: 'dummy-token' }
      },
      error: null
    }),
    signUp: async ({ email }: any) => ({
      data: {
        user: { id: '00000000-0000-0000-0000-000000000000', email: email || 'demo@synexa.com' }
      },
      error: null
    }),
    signOut: async () => ({ error: null })
  }
} as any;

export const supabase = (supabaseUrl && supabaseAnonKey) 
  ? createBrowserClient(supabaseUrl, supabaseAnonKey) 
  : mockSupabase;
