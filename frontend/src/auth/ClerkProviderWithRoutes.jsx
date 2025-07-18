import {ClerkProvider} from "@clerk/clerk-react" //From Clerk's React SDK
import {BrowserRouter} from "react-router-dom"

const PUBLISHABLE_KEY = import.meta.env.VITE_CLERK_PUBLISHABLE_KEY

if (!PUBLISHABLE_KEY) {
  throw new Error('Missing Publishable Key')
}

export default function ClerkProviderWithRoutes({children}) {
    return (
        <ClerkProvider publishableKey="{PUBLISHABLE_KEY}">
            <BrowserRouter>{children}</BrowserRouter>
        </ClerkProvider>
    )
}
/*

Purpose: 
File defines a wrapper component called ClerkProviderWithRoutes which is 
used to wrap the entire react front end app with two providers 

1. ClerkProvider: provides authetication services directly from Clerk
2. BrowserRouter: provides routing (lets your app switch between pages)

The ClerKProviderWithRoutes component takes in a children as prop to wrap it.
The children prop in this case is the entire react app with all components.

ClerkProvider wraps BrowserRouter -> Then BrowserRouter Wraps the <App> component.

*/