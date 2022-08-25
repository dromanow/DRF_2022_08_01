const BookItem = ({book, authors}) => {
    return (
        <tr>
            <td>
                {book.title}
            </td>
            <td>
                {book.authors.map(authorId => authors.find(a => a.id === authorId).last_name) }
            </td>
        </tr>
    )
}

const BookList = ({books, authors}) => {
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
                {books.map((book) => <BookItem book={book} authors={authors}/> )}
            </tbody>
        </table>
    )
}

export default BookList
