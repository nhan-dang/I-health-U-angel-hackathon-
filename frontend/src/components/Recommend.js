import React, { Component } from 'react'
import { from } from 'rxjs'
import { map } from 'rxjs/operators'
import { calculateMacroNutrients, calculateMicroNutrients } from './calculations'

import logo from '../imgs/logo.png'

// Datasets

import nutrients from '../data/nutrients.json'

// Styles
import '../App.css'

export default class Nutritions extends Component {
	state = {}
	nutrients$ = from(nutrients)
	nutrientsLimited$ = from(nutrients).pipe(
		map(nutrient => ({
			name: nutrient.name,
			rda: nutrient.rda,
		})),
	);

	updateNutrients = selectedFoods$ => {
		this.setState({
			macroNutrients: calculateMacroNutrients(selectedFoods$),
			microNutrients: calculateMicroNutrients(selectedFoods$, this.nutrientsLimited$),
		})
	}

	componentDidMount() {
		
	}

	render() {
		console.log('App render');
		return (
			<div className="App">
				{/* Show food nutrients */}
				{/* <div className="rightPanel">
					<MacroNutrients macroNutrients={this.state.macroNutrients} />
					<MicroNutrients definitions={nutrients} microNutrients={this.state.microNutrients} />
				</div> */}
			</div>
		)
	}
}
