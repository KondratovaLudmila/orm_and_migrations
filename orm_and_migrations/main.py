import argparse
from datetime import datetime
from pprint import pprint


from models import db_models
from crud import *



def clean_values(values: dict):
    clean = {}
    for key, value in values.items():
        if value is None:
            continue

        clean[key] = value

    return clean


def add_model_args(parser: argparse.ArgumentParser, model: str, is_required: bool=True):
    match model:
        case "group":
            parser.add_argument("-n", "--name", 
                                type=str, 
                                required=is_required)
        case "teacher":
            parser.add_argument("-n", "--name", 
                                type=str, 
                                required=is_required,
                                dest="full_name")
        
        case "student":
            parser.add_argument("-n", "--name", 
                                type=str, 
                                required=is_required,
                                dest="full_name")
            parser.add_argument("-g", "--group", 
                                type=int, 
                                required=is_required,
                                dest="group_id")
        
        case "subject":
            parser.add_argument("-n", "--name", 
                                type=str, 
                                required=is_required)
            parser.add_argument("-t", "--teacher", 
                                type=int, 
                                required=is_required,
                                dest="teacher_id")
        
        case "mark":
            parser.add_argument("--mark", 
                                type=int, 
                                required=is_required)
            parser.add_argument("-d", "--date", 
                                type=lambda s: datetime.strptime(s, '%d.%m.%Y') , 
                                required=is_required,
                                dest="mark_date")
            parser.add_argument("-std", "--student", 
                                type=int, 
                                required=is_required, 
                                dest="student_id")
            parser.add_argument("-sub", "--subject", 
                                type=int, 
                                required=is_required, 
                                dest="subject_id")
            
    return parser
            

def main():
    parser = argparse.ArgumentParser(description="Cli for database operations")
    parser.add_argument("-a", "--action", 
                        type=str, 
                        choices=["create", "list", "update", "remove"], 
                        required=True,
                        help="For remove action you should additional provide -\
                                only -id argument to specified record to remove")
    parser.add_argument("-m", "--model", 
                        type=str, 
                        choices=db_models.keys(), 
                        required=True,
                        )
    
    args, unparsed = parser.parse_known_args()
    
    values = {}
    command = None
    if args.action == "list":
        value_parser = argparse.ArgumentParser(description=f"Shows records from {args.model} table in database")
        value_parser.add_argument("-id", type=int)
        value_parser = add_model_args(value_parser, args.model, is_required=False)
        values = vars(value_parser.parse_args(unparsed))
        command = read_records
    
    elif args.action == "remove":
        value_parser = argparse.ArgumentParser(description=f"removes record in {args.model} table in database")
        value_parser.add_argument("-id", type=int, required=True)
        values = vars(value_parser.parse_args(unparsed))
        command = remove_record
    
    elif args.action == "update":
        value_parser = argparse.ArgumentParser(description=f"updates record in {args.model} table in database")
        value_parser.add_argument("--id", type=int, required=True)
        group = parser.add_argument_group(f'{args.Model} parameters', 'Provide this arguments for operations with this table')
        parser = group.add_mutually_exclusive_group(required=True)
        value_parser = add_model_args(value_parser, args.model, is_required=False)
        values = vars(value_parser.parse_args(unparsed))
        command = update_record
    
    elif args.action == "create":
        value_parser = argparse.ArgumentParser(description=f"creates record in {args.model} table in database")
        value_parser = add_model_args(value_parser, args.model)
        values = vars(value_parser.parse_args(unparsed))
        command = create_record

    values = clean_values(values)
    try:
         result = command(args.model, values)
    except Exception as error:
        result = str(error)

    if result is None:
        result = "Command successfully executed"

    pprint(result)

if __name__ == "__main__":
    main()

    
