import { NextRequest, NextResponse } from 'next/server';
import NextAuth from 'next-auth';
import { authConfig } from './auth.config';
import { cookies } from 'next/headers'
// import userSignedIn;
const isInMaintenanceMode = true

export default NextAuth(authConfig).auth;

// export function middleware(req: { cookies: { [x: string]: any; }; }) {
//   let res = NextResponse.next();
//   let cookie = req.cookies["session-token"];
//   console.log(cookie);
// }

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|.*\\.png$).*)'],
}

export async function middleware(req: NextRequest) {
  const cookieStore = cookies();
  const userSignedIn = cookieStore.get('authjs.session-token');
    
  // Check Edge Config to see if the maintenance page should be shown

  // If in maintenance mode, point the url pathname to the maintenance page
  if (isInMaintenanceMode && !userSignedIn) {
    req.nextUrl.pathname = `/`

    // Rewrite to the url
    return NextResponse.rewrite(req.nextUrl)
  }
}