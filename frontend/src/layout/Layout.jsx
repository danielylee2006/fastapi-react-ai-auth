import "react"
import {SignedIn, SignedOut, UserButton} from "@clerk/clerk-react"
import {Outlet, Link, Navigate} from "react-router-dom"

export function Layout() {
    return <div className="app-layout">
        <header className="app-header">
            <div className="header-content">
                <h1>Code Challenge Generator</h1>

                <nav>
                    <SignedIn>
                        <Link to="/">Generate Challenge</Link>
                        <Link to="/history">History</Link>
                        <UserButton/>
                    </SignedIn>
                </nav>
            </div>
        </header>

        <main className="app-main"> 
            <SignedOut>
                <Navigate to="/sign-in" replace/>
            </SignedOut>

            <SignedIn>
                <Outlet />
            </SignedIn>
        </main>
    </div>
}

/*

This code determines the layout of the main page (Code Generator Page "/")
and the history page ("/history")

If the User status is "SignedIn", the links in the conditional wrapper "SignedIn" 
will display within the header content div.

Below the page header, there is a main content area. If the User status is SignedOut
we automatically navigate them to /sign-in route
(replace just makes it so that they stay in the current tab instead of creating a new
tab to navigate to the /sign-in route.

If the User status is SignedIn, the Outlet Component is loaded.
<Outlet/> is a placeholder that renders the nested routes. 

For example: lets say the user, navigates to the /history route.

1. Within App.jsx, the Layout Route is run <Route element={<Layout/>}>
2. Within the Layout it finds the corresponding nested Route <Route path="/history" element={<HistoryPannel />} />
3. Inside Layout.jsx it sees: 
<SignedIn>
  <Outlet />
</SignedIn>
4. SO.. it replaces the <Outlet/> placeholder with <HistoryPannel/>

WE WANT TO CREATE A LAYOUT PAGE TO SHARE UI STRUCTURE ACROSS MULTIPLE 
ROUTES/PAGES. IF THE PAGES HAVE SIMILAR LOGIC AND PAGE LAYOUT NEST THEM INSIDE
A LAYOUT PAGE. YOU CAN ACCESS THE NESTED LAYOUT PAGES USING THE OUTLET COMPONENT. 


*/