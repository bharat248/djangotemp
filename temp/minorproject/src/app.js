import axios from 'axios';
import './index.css';
import React, { Component } from 'react';

class App extends Component {
  state = {
    // Initially, no file is selected
    image: null,
  };

  // On file select (from the pop up)
  onFileChange = (event) => {
    // Update the state
    this.setState({ image: event.target.files[0] });
  };

  // On file upload (click the upload button)
  onFileUpload = () => {
    let form_data = new FormData();
    form_data.append('title', this.state.image.name);
    form_data.append('image', this.state.image, this.state.image.name);
    let url = 'http://localhost:8000/api/posts/';
    axios
      .post(url, form_data, {
        headers: {
          'content-type': 'multipart/form-data',
        },
      })
      .then((res) => {
        console.log(res.data);
      })
      .catch((err) => console.log(err));
  };

  // File content to be displayed after
  // file upload is complete
  fileData = () => {
    if (this.state.image) {
      return (
        <div className='center'>
          <h2>File Details:</h2>
          <p>File Name: {this.state.image.name}</p>
          <p>File Type: {this.state.image.type}</p>
          <p>
            Last Modified: {this.state.image.lastModifiedDate.toDateString()}
          </p>
        </div>
      );
    } else {
      return (
        <div className='center'>
          <br />
          <h4>Choose before Pressing the Upload button</h4>
        </div>
      );
    }
  };

  render() {
    return (
      <div className='main'>
        <div className='container'>
          <br></br>

          <h1 className='center'>SMART VEHICLE SURVEILLANCE</h1>
          <br></br>
          <h5 className='center mt-5'>UPLOAD THE IMAGE</h5>
          

          <form className='form-inline'>
            <div className='input-group mb-1'>
              <input
                className='form-control '
                type='file'
                id='formFile'
                onChange={this.onFileChange}
              />

              <button
                type='submit'
                className=' btn btn-primary'
                onClick={this.onFileUpload}
              >
                Upload!
              </button>
            </div>
          </form>

          {/* <div style={{ color: 'white' }}>{this.fileData()}</div> */}
        </div>
      </div>
    );
  }
}

export default App;
