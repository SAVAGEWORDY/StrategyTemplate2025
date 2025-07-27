"""High-level strategy code"""

# !v DEBUG ONLY
import math  # type: ignore
from time import time  # type: ignore
from typing import Optional

from bridge import const
from bridge.auxiliary import aux, fld, rbt  # type: ignore
from bridge.const import State as GameStates
from bridge.router.base_actions import Action, Actions, KickActions  # type: ignore
from bridge.strategy.attacker2 import Attacker2

class Strategy:
    """Main class of strategy"""

    def __init__(
        self,
    ) -> None:
        self.we_active = False
        self.num_point = 1
        self.dist = 5000
        self.attacker2 = Attacker2()
        self.Point0 = 0
        self.Point1 = 0
        self.Point2 = 0
        self.Point3 = 0
        self.Point4 = 0
        self.Point5 = 0
        self.Point6 = 0
        self.Point7 = 0
        self.Point8 = 0
        self.Point9 = 0


    def process(self, field: fld.Field) -> list[Optional[Action]]:
        """Game State Management"""
        if field.game_state not in [GameStates.KICKOFF, GameStates.PENALTY]:
            if field.active_team in [const.Color.ALL, field.ally_color]:
                self.we_active = True
            else:
                self.we_active = False

        actions: list[Optional[Action]] = []
        for _ in range(const.TEAM_ROBOTS_MAX_COUNT):
            actions.append(None)

        if field.ally_color == const.COLOR:
            text = str(field.game_state) + "  we_active:" + str(self.we_active)
            field.strategy_image.print(aux.Point(600, 780), text, need_to_scale=False)
        match field.game_state:
            case GameStates.RUN:
                self.run(field, actions)
            case GameStates.TIMEOUT:
                pass
            case GameStates.HALT:
                return [None] * const.TEAM_ROBOTS_MAX_COUNT
            case GameStates.PREPARE_PENALTY:
                pass
            case GameStates.PENALTY:
                pass
            case GameStates.PREPARE_KICKOFF:
                pass
            case GameStates.KICKOFF:
                pass
            case GameStates.FREE_KICK:
                pass
            case GameStates.STOP:
                # The router will automatically prevent robots from getting too close to the ball
                self.run(field, actions)

        return actions

    def run(self, field: fld.Field, actions: list[Optional[Action]]) -> None:
        """
        ONE ITERATION of strategy
        NOTE: robots will not start acting until this function returns an array of actions,
              if an action is overwritten during the process, only the last one will be executed)

        Examples of getting coordinates:
        - field.allies[8].get_pos(): aux.Point -   coordinates  of the 8th  robot from the allies
        - field.enemies[14].get_angle(): float - rotation angle of the 14th robot from the opponents

        - field.ally_goal.center: Point - center of the ally goal
        - field.enemy_goal.hull: list[Point] - polygon around the enemy goal area


        Examples of robot control:
        - actions[2] = Actions.GoToPoint(aux.Point(1000, 500), math.pi / 2)
                The robot number 2 will go to the point (1000, 500), looking in the direction π/2 (up, along the OY axis)

        - actions[3] = Actions.Kick(field.enemy_goal.center)
                The robot number 3 will hit the ball to 'field.enemy_goal.center' (to the center of the enemy goal)

        - actions[9] = Actions.BallGrab(0.0)
                The robot number 9 grabs the ball at an angle of 0.0 (it looks to the right, along the OX axis)
        """
        #actions[2] = Actions.GoToPointIgnore(aux.point_on_line(field.b_team[0].get_pos(), field.y_team[0].get_pos(), aux.dist(field.b_team[0].get_pos(), field.y_team[0].get_pos()) / 8 * 2), (field.y_team[0].get_pos()-field.b_team[2].get_pos()).arg())
        #actions[2] = Actions.GoToPointIgnore((aux.rotate(aux.Point(500,0), (3.14 / 2)+ (time()/3) )+field.ball.get_pos()), (field.ball.get_pos()-field.b_team[2].get_pos()).arg())
        
        '''
        if self.num_point == 1:
            if aux.dist(aux.nearest_point_in_poly(field.b_team[2].get_pos(), field.ally_goal.hull), field.b_team[2].get_pos()) < aux.dist(aux.nearest_point_in_poly(field.b_team[2].get_pos(), field.enemy_goal.hull), field.b_team[2].get_pos()):
                actions[2] = Actions.GoToPointIgnore(aux.nearest_point_in_poly(field.b_team[2].get_pos(), field.ally_goal.hull), 0)
            else:
                actions[2] = Actions.GoToPointIgnore(aux.nearest_point_in_poly(field.b_team[2].get_pos(), field.enemy_goal.hull), 0)

        if aux.dist(aux.nearest_point_in_poly(field.b_team[2].get_pos(), field.ally_goal.hull), field.b_team[2].get_pos()) < 150 or aux.dist(aux.nearest_point_in_poly(field.b_team[2].get_pos(), field.enemy_goal.hull), field.b_team[2].get_pos()) < 150:
            self.num_point = 2

        if self.num_point == 2:
            actions[2] = Actions.GoToPointIgnore(field.ball.get_pos(), 0)

        if aux.dist(field.ball.get_pos(), field.b_team[2].get_pos()) < 200:
            self.num_point = 1
        '
        self.Point0 = field.y_team[0].get_pos()
        self.Point1 = aux.rotate(aux.Point(self.dist, 0), (field.y_team[0].get_angle())) + field.y_team[0].get_pos()

        self.Point2 = field.b_team[0].get_pos()
        self.Point3 = aux.rotate(aux.Point(self.dist, 0), (field.b_team[0].get_angle())) + field.b_team[0].get_pos()

        self.Point4 = field.y_team[4].get_pos()
        self.Point5 = aux.rotate(aux.Point(self.dist, 0), (field.y_team[4].get_angle())) + field.y_team[4].get_pos()

        field.strategy_image.draw_line(self.Point0, self.Point1, (0, 0, 0), 15)
        field.strategy_image.draw_line(self.Point2, self.Point3, (0, 0, 0), 15)
        field.strategy_image.draw_line(self.Point4, self.Point5, (0, 0, 0), 15)

        self.Point6 = aux.get_line_intersection(self.Point0, self.Point1, self.Point2, self.Point3, "LL")
        self.Point7 = aux.get_line_intersection(self.Point0, self.Point1, self.Point4, self.Point5, "LL")
        self.Point8 = aux.get_line_intersection(self.Point4, self.Point5, self.Point2, self.Point3, "LL")


        if self.Point6 is not None:
            field.strategy_image.draw_circle(self.Point6, (255, 0, 0), 20)
        if self.Point7 is not None:
            field.strategy_image.draw_circle(self.Point7, (255, 0, 0), 20)
        if self.Point8 is not None:
            field.strategy_image.draw_circle(self.Point8, (255, 0, 0), 20)

        if self.Point6 is not None and self.Point7 is not None and self.Point8 is not None:
            self.Point9 = (self.Point6 + self.Point8 + self.Point7)/3
        if self.Point9 is not None:
            #field.strategy_image.draw_circle(self.Point9, (255, 255, 255), 10)
            actions[2] = Actions.GoToPointIgnore(self.Point9, 0)
        
        self.Point0 = field.b_team[0].get_pos()
        self.Point1 = field.ball.get_pos()

        self.Point2 = field.y_team[0].get_pos()
        self.Point3 = field.y_team[5].get_pos()

        self.Point4 = (self.Point1-self.Point0).unity()*1000 + field.ball.get_pos()

        field.strategy_image.draw_line(self.Point0, self.Point2, (255, 255, 0), 10)
        field.strategy_image.draw_line(self.Point0, self.Point3, (255, 255, 0), 10)

        self.Point5 = aux.closest_point_on_line(self.Point1, self.Point3, self.Point4, "L")

        field.strategy_image.draw_line(self.Point4, self.Point5, (255, 255, 0), 15)
        self.Point6 = aux.closest_point_on_line(self.Point0, self.Point2, self.Point4, "L")
        field.strategy_image.draw_line(self.Point4, self.Point6, (255, 0, 255), 30)
        if aux.dist(self.Point4, self.Point6)>aux.dist(self.Point4, self.Point5):
            actions[2] = Actions.GoToPointIgnore(self.Point6, 0)
        else:
            actions[2] = Actions.GoToPointIgnore(self.Point5, 0)
        '''
        
        if field.ally_color == const.Color.BLUE:
            actions[1] = Actions.Kick(field.b_team[2].get_pos())
            self.attacker2.kick(field, actions)
           
            
        else:
        
            '''
             if aux.dist(field.y_team[0].get_pos(), field.enemy_goal.down) > aux.dist(field.y_team[0].get_pos(), field.enemy_goal.up): 
                actions[1] = Actions.Kick(field.enemy_goal.down - aux.Point(0, -100))
            else:
                actions[1] = Actions.Kick(field.enemy_goal.up - aux.Point(0, 100))
            
            self.Point11 = field.b_team[1].get_pos()
            self.Point12 = field.ball.get_pos()

            self.Point22 = (self.Point12 - self.Point11).unity() * 500 + field.ball.get_pos()

            self.Point31 = field.ally_goal.down - aux.Point(0, -100)
            self.Point32 = field.ally_goal.up - aux.Point(0, 100)

            self.Point41 = aux.closest_point_on_line(self.Point11, self.Point31, self.Point22, "L")
            self.Point42 = aux.closest_point_on_line(self.Point11, self.Point32, self.Point22, "L")

            if aux.dist(self.Point22, self.Point41) > aux.dist(self.Point22, self.Point42):
                actions[1] = Actions.GoToPoint(self.Point42, 3.14)
            else:
                actions[1] = Actions.GoToPoint(self.Point41, 3.14) 
            
            self.Point51 = field.ball.get_pos()
            self.Point52 = self.Point51
            self.Point53 = aux.get_line_intersection(self.Point51, self.Point52, field.ally_goal.up - aux.Point(150, -100), field.ally_goal.up - aux.Point(150, 100), "LL")
            if self.Point53 is not None:
                actions[0] = Actions.GoToPointIgnore(self.Point53, 3.14)
            else:
                actions[0] = Actions.GoToPointIgnore(field.ally_goal.center - aux.Point(150, 0), 3.14)

            
        if aux.dist(field.y_team[1].get_pos(), field.enemy_goal.up) > aux.dist(field.y_team[1].get_pos(), field.enemy_goal.down):
            actions[2] = Actions.Kick(aux.Point(0,-75)+field.enemy_goal.up)
        else:
            actions[2] = Actions.Kick(aux.Point(0, 75)+field.enemy_goal.down)
        
        if field.is_ball_moves_to_goal:
            #cto-to
            if aux.dist(field.y_team[1].get_pos(), field.enemy_goal.up) > aux.dist(field.y_team[1].get_pos(), field.enemy_goal.down):
                actions[2] = Actions.Kick(aux.Point(0,-75)+field.enemy_goal.up)
            else:
                actions[2] = Actions.Kick(aux.Point(0, 75)+field.enemy_goal.down)
        else:
            actions[1] = Actions.GoToPointIgnore(field.ally_goal.center + aux.Point(400,0), 0)
        

        self.Point52 = aux.nearest_point_in_poly(field.ball.get_pos(), field.ally_goal.hull)
        actions[const.GK] = Actions.GoToPointIgnore(self.Point52, 0)
            '''
        

        
        

