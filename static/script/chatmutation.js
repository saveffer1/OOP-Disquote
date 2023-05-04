import { gql } from 'graphql-tag';

const SEND_MESSAGE_MUTATION = gql`
  mutation SendMessage($sender: String!, $content: String!, $date: String!) {
    sendMessage(sender: $sender, content: $content, date: $date) {
      id
      sender
      content
      date
    }
  }
`;
