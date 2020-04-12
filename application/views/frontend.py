"""

"""
from aiohttp_jinja2 import template
from aiohttp import web
from ..database import base
import asyncio
from ..image_processing.img_handler import get_image_url
from ..concurrency import make_task, start_delete_delay, get_previous_task


class Index(web.View):
    """Class which handles index.html

    Basic page. Renders templates using aiohttp_jinja2.

    """
    @template('index.html')
    async def get(self):
        token_list = await base.get_all_tokens(self.app)

        return {'token_list': token_list}


class Token(web.View):

    async def post(self):
        """Token processing
         Within this function we handle a token. We check a token for the accuracy.
         There are 4 options:
         1) Token is integrally proper and we return an image (image url)
         2) Such token exists but it's not at first position then we return error with appropriating status
         3) Such token doesn't exist hence return cheating-error
         4) Data base is empty. This status was created for my own purposes, it's 3d option indeed.
        """
        # Receive the data from the request
        post_data = await self.post()

        # The response depended on post_data accuracy.
        response = {}

        # delete_token_from_db() makes an effort to delete the token from db
        # It returns two values:
        # 1) token_availability -- Is the token in database? (True/False)
        # 2) token_accuracy -- Does the token coincide with the first token. It receives (True/False) except the case
        #                      when the data base empty in this way it appears as the string ('Table is empty')
        token_availability, token_accuracy = await base.delete_token_from_db(self.app, post_data['token-field'])

        # Check for the database emptiness
        if token_accuracy != 'Table is empty':

            # First case, whether the needed toke is first one?
            if token_availability and token_accuracy:

                # How do I close a task? Follow link below:
                # https://stackoverflow.com/questions/56823893/how-to-get-task-out-of-asyncio-event-loop-in-a-view
                if closing_task := get_previous_task():
                    closing_task.cancel()

                # If the token is first then we shall to prepare it for the reuse.
                # The prepare_used_token() is placed at ../application/QMS/tokengenerator.py
                self.app['new_token'].prepare_used_token(post_data['token-field'])

                # Start the timer for the next token
                # If user used his/her/its token until the out of the time I want to close the task of the time counting
                # Therefore I using the function of creating the task placed at
                # ../application/concurrency/taskconfigurator.py
                if not await base.db_empty(self.app):
                    task = make_task(start_delete_delay, self.app, 60)
                    asyncio.gather(task)

                # Generate an image
                img_url = get_image_url()
                response.update({'status': 'success'})
                response.update({'image_url': img_url})

            # The option where token is not first.
            elif token_availability:
                response.update({'status': 'wrong_turn'})

            # The option where token is not within the queue.
            else:
                response.update({'status': 'cheater'})

        # The option where no tokens in database
        else:
            response.update({'status': 'db_empty'})

        return web.json_response(response)

    async def get(self):
        """Generate token and represent it.

        returns a generated token and its position for the js func.
        """

        # We need this check to get a point about # of call.
        # If it's 1st call therefore we need start delay task.
        # If it's not then we skip the delay starting.
        db_emptiness = await base.db_empty(self.app)

        # Generating & Inserting into database a token
        token = self.app['new_token'].generate_new_token()
        await base.insert_token_into_db(self.app, token)

        # Creating the first task for the token' popping
        if db_emptiness:
            task = make_task(start_delete_delay, self.app, 60)
            asyncio.gather(task)

        # retrieving a token position for the js function (display_queue_add)
        token_position = await base.get_num_of_tokens(self.app)

        return web.json_response({'token': token, 'token_position': token_position[0]['count_1']})
