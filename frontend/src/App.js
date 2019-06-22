import React from "react";
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import Nutritions from './components/Nutritions.js';
import Recommend from './components/Recommend.js';
import Login from './components/Login';

export default function App() {
	return (
	  <Router>
		<div>
		  <ul>
			<li>
			  <Link to="/">Login</Link>
			</li>
			<li>
			  <Link to="/#">About</Link>
			</li>
			<li>
			<Link to="/recommend">Recommend System</Link>
			</li>
		  </ul>
  
		  <hr />
  
		  <Route exact path="/" component={Login} />
		  <Route exact path="/nutritions" component={Nutritions}/>
		  <Route exact path="/recommend" component={Recommend}/>
		  {/* <Route path="/nutritions" component={About} />
		  <Route path="/topics" component={Topics} /> */}
		</div>
	  </Router>
	);
  }