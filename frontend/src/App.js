import React from "react";
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import Nutritions from './components/Nutritions.js';
import Recommend from './components/Recommend.js';
import Login from './components/Login';

import ChooseForm from "./components/ChooseForm.js";


import Test from './components/Test.js';
export default function App() {
	return (
	  <Router>
		<div>
		  <ul>
			<li>
			  <Link to="/">Login</Link>
			</li>
			{/*<li>
			  <Link to="/#">About</Link>
			</li>*/}
			<li>
			<Link to="/recommend">Recommend System</Link>
			</li>

			<li>
			<Link to="/familymeal">Choose your Family meal</Link>
			</li>
              {/*<li>
			<Link to="/test">Test get JSON</Link>
			</li>*/}
		  </ul>
  
		  <hr />
  
		  <Route exact path="/" component={Login} />
		  <Route exact path="/nutritions" component={Nutritions}/>
		  <Route exact path="/recommend" component={Recommend}/>

		  <Route exact path="/familymeal" component={ChooseForm}/>
            <Route exact path="/test" component={Test}/>
		  {/* <Route path="/nutritions" component={About} />
		  <Route path="/topics" component={Topics} /> */}

		</div>
	  </Router>
	);
  }