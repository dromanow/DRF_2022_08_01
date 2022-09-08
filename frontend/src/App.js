import React from 'react'
import axios from 'axios'
import AuthorList from './components/AuthorList.js'
import BookList from './components/BookList.js'
import AuthorBookList from './components/AuthorBookList.js'
import LoginForm from './components/LoginForm.js'
import BookForm from './components/BookForm.js'
import {HashRouter, BrowserRouter, Route, Routes, Link, Navigate, useLocation, useNavigate} from 'react-router-dom'


const NotFound = () => {
    var {pathname} = useLocation()

    return (
        <div>
            Page "{pathname}" not found
        </div>
    )
}

class App extends React.Component {
    constructor(props) {
        super(props)

        this.state = {
            'authors': [],
            'books': [],
            'token': '',
            'redirect': false
        }
    }

    deleteBook(bookId) {
        let headers = this.getHeaders()

        axios
            .delete(`http://127.0.0.1:8000/api/books/${bookId}`, {headers})
            .then(response => {
                this.setState({
                    'books': this.state.books.filter((book) => book.id != bookId)
                })
            })
            .catch(error => {
                console.log(error)
            })
//        console.log(bookId)
    }

    createBook(title, authors) {
//        console.log(title, authors)

        let headers = this.getHeaders()

        axios
            .post('http://127.0.0.1:8000/api/books/', {'title': title, 'authors': authors}, {headers})
            .then(response => {
                this.setState({
                    'redirect': '/books'
                }, this.getData)
            })
            .catch(error => {
                console.log(error)
            })
    }

    obtainAuthToken(login, password) {
        axios
            .post('http://127.0.0.1:8000/api-auth-token/', {
                'username': login,
                'password': password
            })
            .then(response => {
                const token = response.data.token
                console.log('token:', token)
                localStorage.setItem('token', token)

                this.setState({
                    'token': token,
                    'redirect': '/'
                }, this.getData)
            })
            .catch(error => console.log(error))
    }

    isAuth() {
        return !!this.state.token
    }

    componentDidMount() {
        let token = localStorage.getItem('token')
        this.setState({
            'token': token
        }, this.getData)
    }

    getHeaders() {
        if (this.isAuth()) {
            return {
                'Authorization': 'Token ' + this.state.token
            }
        }
//        return { 'Accept': 'application/json; version=2.0' }
        return { }
    }

    getData() {
        this.setState({
            'redirect': false
        })

        let headers = this.getHeaders()

        axios
            .get('http://127.0.0.1:8000/api/authors/', {headers})
            .then(response => {
                const authors = response.data
                this.setState({
                    'authors': authors
                })
            })
            .catch(error => {
                console.log(error)
                this.setState({ 'authors': [] })
            })
        axios
            .get('http://127.0.0.1:8000/api/books/', {headers})
            .then(response => {
                const books = response.data
                this.setState({
                        'books': books
                    })
            })
            .catch(error => {
                console.log(error)
                this.setState({ 'books': [] })
            })
    }


    logOut() {
        localStorage.setItem('token', '')
        this.setState({
            'token': '',
        }, this.getData)
    }

//    http://localhost:3000/#/books
//    http://localhost:3000/
//    http://localhost:3000/books

    render() {
        return (
            <div>
                <BrowserRouter>
                    {this.state.redirect ? <Navigate to={this.state.redirect} /> : <div/>}

                    <nav>
                        <li> <Link to='/'>Authors</Link> </li>
                        <li> <Link to='/books'>Books</Link> </li>
                        <li> <Link to='/create_book'>Create book</Link> </li>
                        <li>
                        {this.isAuth() ? <button onClick={() => this.logOut()}>Logout</button> : <Link to='/login'>Login</Link> }
                        </li>
                    </nav>

                    <Routes>
                        <Route exact path='/' element={<Navigate to='/authors' />} />
                        <Route exact path='/books' element={<BookList books={this.state.books} authors={this.state.authors} deleteBook={(bookId) => this.deleteBook(bookId)} />} />
                        <Route exact path='/create_book' element={<BookForm authors={this.state.authors} createBook={(title, authors) => this.createBook(title, authors)} />} />
                        <Route exact path='/login' element={<LoginForm obtainAuthToken={(login, password) => this.obtainAuthToken(login, password)} />} />
                        <Route path='/authors'>
                            <Route index element={<AuthorList authors={this.state.authors} />} />
                            <Route path=':authorId' element={<AuthorBookList books={this.state.books} />} />
                        </Route>
                        <Route path='*' element={<NotFound />} />
                    </Routes>
                </BrowserRouter>
            </div>
        )
    }
}

export default App;
