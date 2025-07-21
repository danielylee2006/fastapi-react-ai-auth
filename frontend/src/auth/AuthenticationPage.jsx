import "react";
import { SignIn, SignUp, SignedIn, SignedOut } from "@clerk/clerk-react";

export function AuthenticationPage() {
  return (
    <div className="auth-container">
      <SignedOut>
        <SignIn routing="path" path="/sign-in" />
        <SignUp routing="path" path="/sign-up" />
      </SignedOut>

      <SignedIn>
        <div className="redirect-message">
            <p>You are already signed in.</p>
        </div>
      </SignedIn>
    </div>
  );
}

/*

- auth-container div is simply a wrapper div for styling

- routing property is set to "path" which tells clerk to use
path based routing.

- Match the wanted router path to right component.

-SignedIn and SignedOut are CONDITIONAL WRAPPERS not PHYSICAL COMPONENTS
- Think of them like if statements:
    - If user is SignedOut -> render Signin or Signout page based on path routing
    - If user is SignedIn -> Render paragraph "already signed in"


*/
