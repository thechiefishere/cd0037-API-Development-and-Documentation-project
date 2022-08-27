import React, { Component } from 'react';
import '../stylesheets/Login.css';

export default class Login extends Component {
  constructor(props) {
    super(props);

    this.state = {
      username: '',
      password: '',
    };
  }

  navTo(uri) {
    window.location.href = window.location.origin + uri;
  }

  renderLogin() {
    return (
      <section className='Login-Component'>
        <div className='Component-Heading'>
          <h1>LOGIN</h1>
          <p>Enter your account details</p>
        </div>
        <form className='Form'>
          <div className='Form-Component'>
            <label>Username:</label>
            <input
              type='text'
              placeholder='Enter your username'
              value={this.state.username}
              onChange={(e) => this.setState({ username: e.target.value })}
            />
          </div>
          <div className='Form-Component'>
            <label>Password:</label>
            <input
              type='password'
              placeholder='Enter your password'
              value={this.state.password}
              onChange={(e) => this.setState({ password: e.target.value })}
            />
          </div>
          <input type='submit' value='Login' />
        </form>
        <div className='Login-Nav'>
          <p>Don't have an account?</p>
          <p
            onClick={() => {
              this.navTo('/signup');
            }}
          >
            SignUp
          </p>
        </div>
      </section>
    );
  }

  render() {
    return <div className='Login'>{this.renderLogin()}</div>;
  }
}
