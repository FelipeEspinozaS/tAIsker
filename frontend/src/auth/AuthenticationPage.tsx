import "react"
import { SignIn, SignUp, SignedIn, SignedOut } from "@clerk/clerk-react";

export function AuthenticationPage() {
  return <div className="authentication-page">
    <SignedOut>
      <SignIn path="/signin" routing="path" signUpUrl="/signup" />
      <SignUp path="/signup" routing="path" signInUrl="/signin" />
    </SignedOut>
    <SignedIn>
      <div className="signed-in-message">
        You are signed in!
      </div>
    </SignedIn>
  </div>;
}