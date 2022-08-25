import {useParams} from 'react-router-dom'


const BookItem = ({book}) => {
    return (
        <tr>
            <td>
                {book.title}
            </td>
            <td>
                {book.authors}
            </td>
        </tr>
    )
}

const AuthorBookList = ({books}) => {
    var {authorId} = useParams()
    var filteredBooks = books.filter((book) => book.authors.includes(parseInt(authorId)))

    return (
        <table>
            <thead>
                <tr>
                    <th>
                        Title
                    </th>
                    <th>
                        Authors
                    </th>
                </tr>
            </thead>
            <tbody>
                {filteredBooks.map((book) => <BookItem book={book} /> )}
            </tbody>
        </table>
    )
}

export default AuthorBookList
