import type { NextAuthConfig } from 'next-auth';

export const authConfig = {
  trustHost: true,
  secret: process.env.NEXTAUTH_SECRET,
  pages: {
    signIn: '/login'
  },
  providers: [],
  callbacks: {
    authorized({ auth, request: { nextUrl } }) {
      console.log('AUTHORIZATION PORTION');
      const isLoggedIn = !!auth?.user;
      
      const isOnDashboard = nextUrl.pathname.startsWith('/dashboard');
      if (isOnDashboard) {
        console.log(`isOnDashboard: ${isOnDashboard}`);
        if (isLoggedIn) return true;
        console.log('incorrect credentials');
        
        return false; // Redirect unauthenticated users to login page
      } else 
      if (isLoggedIn) {
        console.log(`isLoggedIn2: ${isLoggedIn}`);
        console.log('correct credentials');
        return Response.redirect(new URL('/dashboard', nextUrl));
      }
      return true;
    },
  },
} satisfies NextAuthConfig;