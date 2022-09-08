const BookItem = ({book, authors, deleteBook}) => {
    return (
        <tr>
            <td>
                {book.title}
            </td>
            <td>
                {book.authors.map(authorId => authors.find(a => a.id === authorId).last_name) }
            </td>
            <td>
                <button onClick={() => deleteBook(book.id) }>Delete</button>
            </td>
        </tr>
    )
}

const BookList = ({books, authors, deleteBook}) => {
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
                {books.map((book) => <BookItem book={book} authors={authors} deleteBook={deleteBook}/> )}
            </tbody>
        </table>
    )
}

export default BookList
