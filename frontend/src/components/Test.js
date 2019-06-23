import React, { Component } from 'react';
import axios from "axios";

const URL = "http://localhost:5000/api/test";

export default class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
            json: JSON

        }
    }

    componentDidMount() {
        axios.get(URL)
            .then(res => {
                this.setState({
                    json: JSON.parse(JSON.stringify(res.data))
                });
            })
            .catch(function (e) {
                console.log("ERROR ", e);
            })
    }

    render() {
        console.log(this.state.json)
        return ''
    }
}

