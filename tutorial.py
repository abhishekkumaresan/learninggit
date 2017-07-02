# Sample Test Application which does nothing
# from openerp import fields, models, api


from openerp.osv import fields, osv
from openerp.tools.translate import _

'''
class TutorialProductTemplate(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'
    calories = fields.Integer("calories")
    nutrient_ids = fields.One2many('product.template.nutrient', 'product_id', 'Nutrient')



class TutorialResUsersMeal(models.Model):
    _name = 'res.users.meal'
    meal_name = fields.Char('Meal Name')
    meal_date = fields.Datetime('Menu Date')
    user_id = fields.Many2one('res.users', 'Meal User')
    item_ids = fields.One2many('res.users.mealitem', 'meal_id')
    large_meal = fields.Boolean('Large Meal',compute='check_total_calories')
    total_calories = fields.Integer(string="Total Calories", store=True, compute='_calcalories')
    notes = fields.Text('Model Notes')
    # selection = fields.Selection([('yes', 'Yes'), ('no', 'No')], string="Selection")
    # state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm')], string="State")
    # address=fields.Char('Address')

    @api.one
    @api.depends('item_ids', 'item_ids.servings')
    def _calcalories(self):
        tut = 0
        print(self.item_ids)
        for meal in self.item_ids:
            tut += meal.calories * meal.servings
        self.total_calories = tut

    @api.onchange(total_calories)
    def check_total_calories(self):
        print "check print"
        if self.total_calories > 500:
            self.large_meal = True
        else:
            self.large_meal = False


class TutorialResUsersMealItem(models.Model):
    _name = 'res.users.mealitem'
    meal_id = fields.Many2one('res.users.meal')
    servings = fields.Float('Servings')
    calories = fields.Integer(related="item_id.calories", string="Calories Per Serving", store=True, readonly=True)
    item_id = fields.Many2one('product.template', 'Meal Item')



class TutorialProductNutrient(models.Model):
    _name = 'product.nutrient'
    name = fields.Char('Nutrient Name')
    uom_id = fields.Many2one('product.uom', 'Units of Measurement')


class TutorialProductTempalteNutrient(models.Model):
    _name = 'product.template.nutrient'
    nutrient_id = fields.Many2one('product.nutrient', string='Product Nutrient')
    product_id = fields.Many2one('product.template')
    uom = fields.Char(related="nutrient_id.uom_id.name", String="UOM", readonly=True)
    value = fields.Float('Nutrient Value')
    daily_recomended = fields.Float('Daily Recommended Value')


'''


class TutorialProductTemplate(osv.osv):
    _name = 'product.template'
    _inherit = 'product.template'
    _columns = {
        'calories': fields.integer("calories"),
        'nutrient_ids': fields.one2many('product.template.nutrient', 'product_id', 'Nutrient')
    }


class TutorialResUsersMeal(osv.osv):
    _name = 'res.users.meal'

    def get_customer(self, cr, uid, context=None):

        print ('Printing from get_customer')
        search = self.pool.get('res.partner').search(cr, uid, [('name', '=', 'Cus 1')])
        for temp in self.pool.get('res.partner').browse(cr, uid, search):
            print ('search' ,search)
            print ('temp', temp.mobile)

        return temp.id

        # def check_total_calories(self):
        #     print "check print"
        #     d = {}
        #     if self.total_calories > 500:
        #         self.large_meal = True
        #     else:
        #         self.large_meal = False
        #     d.update({'large_meal': self.large_meal})

        # @api.one
        # @api.depends('item_ids', 'item_ids.servings')

    def cal_calories(self, cr, uid, ids, item_ids, context=None):
        tut = 0
        print ('\n\n\nFrom on change\n\n\n')
        print ('item_ids', item_ids)
        for meals in item_ids:
            if len(meals) >1:
                for meal in meals:
                    search = self.pool.get('res.users.mealitem').search(cr, uid, [('meal_id', '=', meal)])
                    meal_record = self.pool.get('res.users.mealitem').browse(cr, uid, search)
                    tut += meal_record.calories * meal_record.servings
            else:
                search = self.pool.get('res.users.mealitem').search(cr, uid, [('meal_id', '=', meals)])
                meal_record = self.pool.get('res.users.mealitem').browse(cr, uid, search)
                tut += meal_record.calories * meal_record.servings
            # print meal

        return {'total_calories': tut}

    _columns = {
        'meal_name': fields.char('Meal Name'),
        'meal_date': fields.datetime('Menu Date'),
        'user_id': fields.many2one('res.users', 'Meal User'),
        'cus_id': fields.many2one('res.partner', 'Meal Customer'),
        'address': fields.char('Address'),
        'item_ids': fields.one2many('res.users.mealitem', 'meal_id'),
        'large_meal': fields.boolean('Large Meal'),
        # 'total_calories': fields.function(cal_calories, string='Total calories', type='float'),
        'total_calories': fields.float('Total calories'),
        'notes': fields.text('Model Notes'),
        'selection': fields.selection([('yes', 'Yes'), ('no', 'No')], string="Selection"),
        'state': fields.selection([('draft', 'Draft'), ('confirm', 'Confirm')], string="State")

    }

    def test_button_function(self, cr, uid, ids, context=None):
        # This function is called when the 'confirm' object button is clicked
        print "Object Button"
        self.write(cr, uid, ids, {'large_meal': True, 'state': 'confirm'})
        return True

    def create(self, cr, uid, vals, context=None):
        print ('From create method \n\n\n')
        print("vals", vals)
        button = super(TutorialResUsersMeal, self).create(cr, uid, vals)
        return button

    def write(self, cr, uid, ids, vals, context=None):

        print ('From write method \n\n\n')
        print ('vals_write', vals)
        print('ids', ids)
        browse = self.browse(cr, uid, ids)
        print browse.address
        return super(TutorialResUsersMeal, self).write(cr, uid, ids, vals)

    def unlink(self, cr, uid, ids, context=None):

        print ('From create method \n\n\n')
        print ('del_ids', ids)
        raise osv.except_osv(_('Warning!'), _('Not able to delete'))
        super(TutorialResUsersMeal, self).unlink(cr, uid, ids)

    def onchange_fun(self, cr, uid, ids, cus_id, context=None):
        res = {}
        if cus_id:
            # print('cus_id',cus_id)
            b = self.pool.get('res.partner').browse(cr, uid, cus_id)
            print b.street
            res = {'address': b.street}
        return {'value': res}

    _defaults = {
        'meal_name': 'Lunch',
        'meal_date': fields.datetime.now,
        'user_id': lambda obj, cr, uid, context: uid,
        'cus_id': get_customer,
        'state': 'draft'

    }


class TutorialResUsersMealItem(osv.osv):
    _name = 'res.users.mealitem'

    def calc_prod(self, cr, uid, ids, field_name, arg, context=None):
        print ('Printing from calc_prod\n\n\n')
        print ("Cursor", cr)
        print ("ids", ids)
        print ("uid", uid)

        d = {}
        prod = 0.0
        prod1 = 0.0

        # Browsing current class
        for cur_class in self.browse(cr, uid, ids):
            # print ("cur_class", cur_class)
            # print ("cur_class.calories", cur_class.calories)
            # print ("cur_class.servings", cur_class.servings)
            # self.calories * self.servings
            prod = cur_class.calories * cur_class.servings
            prod1 = cur_class.calories + cur_class.servings
            # print ("cur_class.id", cur_class.id)

            # print ("prod", prod, prod1)
            # print ("d", d)
            d[cur_class.id] = {'product_1': prod1, 'product': prod}
        return d

    _columns = {
        'meal_id': fields.many2one('res.users.meal'),
        'servings': fields.float('Servings'),
        'calories': fields.integer(related="item_id.calories", string="Calories Per Serving", store=True,
                                   readonly=True),
        'item_id': fields.many2one('product.template', 'Meal Item'),
        'product': fields.function(calc_prod, string='Product', type='float', multi="prod"),
        'product_1': fields.function(calc_prod, string='Product1', type='float', multi="prod")

    }


class TutorialProductNutrient(osv.osv):
    _name = 'product.nutrient'
    _columns = {
        'name': fields.char('Nutrient Name'),
        'uom_id': fields.many2one('product.uom', 'Units of Measurement')
    }


class TutorialProductTempalteNutrient(osv.osv):
    _name = 'product.template.nutrient'
    _columns = {
        'nutrient_id': fields.many2one('product.nutrient', string='Product Nutrient'),
        'product_id': fields.many2one('product.template'),
        'uom': fields.char(related="nutrient_id.uom_id.name", String="UOM", readonly=True),
        'value': fields.float('Nutrient Value'),
        'daily_recomended': fields.float('Daily Recommended Value')
    }
