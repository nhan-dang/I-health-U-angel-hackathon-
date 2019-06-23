import React from 'react';
import { Button, Input, Checkbox } from 'antd';

class ChooseForm extends React.Component {
    constructor() {
        super();
    }
    state = {
        username: '',
        email: '',
        password: '',
        isAdmin: false,
    }

    onChange(e) {
        this.setState({
            [e.target.name]: e.target.value
        });
    }

    onSubmit(e) {
        e.preventDefault();

        fetch(this.props.formAction, {
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({description: this.state.description})
        });

        this.setState({description: ''});
    }

    render() {
        return (
                <div align="center">
                <form
                    id="main-login"
                    action={this.props.action}
                    method={this.props.method}
                    onSubmit={this.onSubmit}>
                    <h2>I HEALTH U</h2>
                    <label>
                        <span class="text">Number of people</span><br/>
                        <input type="text" name="countPeople"/><br/>
                        <span class="text">Fat</span><br/>
                        <input type="text" name="fat"/><br/>
                        <span class="text">Protein</span><br/>
                        <input type="text" name="protein"/><br/>
                        <span class="text">Carbonhydrates</span><br/>
                        <input type="text" name="carbon"/><br/>
                        <div class="align-right">
                            <button>Submit</button>
                        </div>
                    </label>
                    </form>
            </div>
        );
    }

}

// App.propTypes = { action: React.PropTypes.string.isRequired, method: React.PropTypes.string}
ChooseForm.defaultProps = {
    action: '#',
    method: 'post'
};


export default ChooseForm;