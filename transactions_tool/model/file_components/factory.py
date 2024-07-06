from .footer.footer import Footer
from .header.header import Header
from .transaction.transaction import Transaction


class FileComponentFactory:
    @staticmethod
    def file_component_from_line(line):
        field_id = line[0:2]

        match field_id:
            case Header.FIELD_ID:
                return Header.from_line(line)
            case Transaction.FIELD_ID:
                return Transaction.from_line(line)
            case Footer.FIELD_ID:
                return Footer.from_line(line)

        raise ValueError(f"Line has invalid field_id: {field_id}")
